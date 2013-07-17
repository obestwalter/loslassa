#!/usr/bin/env python
"""
Loslassa
========

Workflow
--------

Start
'''''
**not implemented yet**

::

    loslassa start */path/to/project*

Creates a new project with a basic structure and configuration
similar to sphinx-quickstart only simpler and tailored to only HTML output.

Play
''''
Playing with the source and create your page. Add content and see the
changes right away thanks to local server with automatic
rebuild of the web pages::

::

    cd */path/to/project*
    loslassa play

Starts a local development server reachable on http://localhost:8080.
All files in project folder are being watched and if something changes
the project is rebuild.

Publish
'''''''
**not implemented yet**

This part is a bit vague still but basically it should simply push the
generated pages to the server, by maintaining them in a git repository

First time publishing would clone the repository bare to the web space and
set it to be origin from then on
... or summin like that, didn't think that through yet::

    cd */path/to/project*
    loslassa loslassa

Customize
'''''''''
This is not thought out yet, but I imagine that additional customization
can be done easily by expanding the settings in the sphinx conf.py and
do more involved stuff via sphinx extensions.
"""
from __future__ import print_function

import logging
import sys

from plumbum import cli, cmd, local
import plumbum.utils as plumbum_utils

from devserver import serve_with_reloader
from utils import *


LOSLASSA = "loslassa"
__version__ = '0.3.2-dev'


log = logging.getLogger()


class LoslassaProject(object):
    SPHINX_CONFIG = "conf.py"
    HERE = local.path(__file__).dirname
    PROJECTS = HERE/"projects"
    EXAMPLE_PROJECT = PROJECTS/"example"
    SKELETON_PROJECT = PROJECTS/"skeleton"

    def __init__(self, projectPath):
        assert projectPath, "No project path set"
        self.inputContainer = local.path(local.cwd/projectPath)
        self.projectName = self.inputContainer.basename
        self.sphinxConfig = self.inputContainer/self.SPHINX_CONFIG
        self.buildPath = local.path(self.inputContainer/"__build")
        self.doctreesPath = self.buildPath/"doctrees"
        self.outputPath = self.buildPath/"html"
        log.info(
            "initialized paths: input from %s - html generated in %s" %
            (self.inputContainer, self.outputPath))

    def __str__(self):
        return simple_dbg(self)

    def __repr__(self):
        return "%s(%s)" % (self.__class__.__name__, self.inputContainer)

    def create_project(self):
        plumbum_utils.copy(self.SKELETON_PROJECT, self.inputContainer)

    @property
    def sphinxInvocation(self):
        return cmd.sphinx_build[
            "-b", "dirhtml", "-d", self.doctreesPath._path,
            self.inputContainer._path, self.outputPath._path]


class LoslassaCliApplication(cli.Application):
    PROGNAME = LOSLASSA
    VERSION = __version__
    USAGE = LOSLASSA + " [start|play|loslassa] [OPTIONS]"
    projectPath = None
    logLevel = logging.DEBUG
    logFilePath = None

    def __str__(self):
        return simple_dbg(
            self, excludeNames=["parent", "nested_command"])

    @cli.autoswitch(str)
    def project_name(self, projectName):
        """Set name (can be a relative or absolute path as well"""
        self.projectPath = local.path(projectName)

    @cli.autoswitch(str)
    def verbosity(self, level):
        """Adjust the talkativeness of loslassing activities.

        :param str level: log level (one of the accepted logging values)
        Levels from very chatty to almost silent: debug, info, warning, error
        """
        self.logLevel = level

    @cli.autoswitch(str)
    def log_to_file(self, filePath):
        """Log to a file instead of the console"""
        self.logFilePath = filePath

    def _init(self, create=False):
        if not self.projectPath:
            log.warning("no conf.py here ... searching (press CTRL-C to stop)")
            confPath = find_file(local.cwd, LoslassaProject.SPHINX_CONFIG)
            self.projectPath = confPath.dirname.up()
        self.project = LoslassaProject(self.projectPath)
        if create:
            self.project.create_project()
        adjust_log(level=self.logLevel, filePath=self.logFilePath)
        log.info("working with project '%s'" % (self.project.projectName))
        if log.getEffectiveLevel() > logging.DEBUG:
            sys.excepthook = friendly_exception_handler


class Loslassa(LoslassaCliApplication):
    def main(self, *args):
        log.debug("executing command %s" % str(self.nested_command))
        if args:
            log.error("unknown command %r" % (args[0]))
            return 1

        if not self.nested_command:
            log.error("Which kind of loslassing? "
                      "Try %s --help" % (Loslassa.PROGNAME))
            return 1


@Loslassa.subcommand("start")
class LoslassaStart(LoslassaCliApplication):
    """Starts a new project by creating the initial project structure"""
    def main(self):
        log.info("start loslassing ...")
        if not self.projectPath:
            raise LoslassaError("please provide a name for the project")

        if self.projectPath.exists():
            raise LoslassaError(
                "'%s' already exists (try a different name?)." %
                (self.projectPath.basename))

        self._init(create=True)
        log.info("Created project '%s' at %s" %
                 (self.project.projectName, self.project.inputContainer))


@Loslassa.subcommand("play")
class LoslassaPlay(LoslassaCliApplication):
    """Start playing with the source and create your page"""
    serverPort = 8080

    @cli.autoswitch(int)
    def serve_on_port(self, serverPort):
        """Set port manually"""
        self.serverPort = serverPort

    def main(self):
        """Create the project representation and start serving"""
        self._init()
        log.info("play loslassing...")
        # fixme reloader reloads main method instead just the server!?
        if not self.project.sphinxConfig.exists():
            raise LoslassaError(
                "no config found at %s" % (self.project.sphinxConfig))
        serve_with_reloader(
            serveFromPath=str(self.project.outputPath),
            port=self.serverPort,
            changedCallback=self.project.sphinxInvocation,
            pathToWatch=self.project.inputContainer,
            pathToIgnore=self.project.buildPath)


@Loslassa.subcommand(LOSLASSA)
class LoslassaLoslassa(LoslassaCliApplication):
    """Practice loslassing by pushing your page into the interwebs"""
    def main(self):
        self._init(create=True)
        # todo make a progress bar consisting of loslassa :)
        log.info("loslassa loslassa loslassa ...")
        #raise LoslassaError("coming soon...")


def main():
    logging.basicConfig(level=logging.INFO, format='%(message)s')
    if len(sys.argv) == 1:
        log.info("no args ... using test config instead")
        name = "/home/obestwalter/projects/bilderwerkstatt_ravensburg.de"
        #name = "new"
        ##import shutil
        #shutil.rmtree(name, ignore_errors=True)
        if not local.path(name).exists():
            raise Exception("boo")
            #lp = LoslassaProject(name)
            #lp.create_project()
        args = ["play", "--verbosity", "DEBUG", "--project-name", name]
        sys.argv.extend(args)
    Loslassa.run()


if __name__ == "__main__":
    sys.exit(main())
