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

from plumbum import cli, cmd, local, utils as plum_utils
from plumbum.local_machine import LocalPath

from devserver import serve_with_reloader
from utils import *


LOSLASSA = "loslassa"
__version__ = '0.3.2-dev'


log = logging.getLogger()


class LoslassaProject(object):
    SOURCE_DIR_NAME = "source"
    CONF_FILE_NAME = "conf.py"
    BUILDS_DIR_NAME = "build"
    HTML_BUILD_DIR_NAME = "html"
    DOCTREES_DIR_NAME = "doctrees"
    EXAMPLE_PROJECT_NAME = "example_project"
    EXAMPLE_PROJECT_PATH = LocalPath(__file__).dirname/EXAMPLE_PROJECT_NAME

    def __init__(self, projectPath):
        assert projectPath, "No project path set"
        self.projectPath = LocalPath(projectPath)
        assert self.projectPath.exists
        self.projectName = self.projectPath.basename
        self.sourcePath = self.projectPath/self.SOURCE_DIR_NAME
        self.sphinxConfFilePath = self.sourcePath/self.CONF_FILE_NAME
        self.buildPath = self.projectPath/self.BUILDS_DIR_NAME
        self.doctreesPath = self.buildPath/self.DOCTREES_DIR_NAME
        self.outputPath = self.buildPath/self.HTML_BUILD_DIR_NAME

    def __str__(self):
        return simple_dbg(self, excludeNames=["allPaths"])

    def __repr__(self):
        return "<%s at %s>" % (self.__class__.__name__, self.projectPath)

    def create_empty_project(self):
        for thisPath in self.neededDirPaths:
            thisPath.mkdir()
        confSkelPAth = (
            self.EXAMPLE_PROJECT_PATH/self.SOURCE_DIR_NAME/self.CONF_FILE_NAME)
        plum_utils.copy(confSkelPAth, self.sphinxConfFilePath)

    @property
    def buildCommand(self):
        return cmd.sphinx_build[
            "-b", "dirhtml", "-d", self.doctreesPath._path,
            self.sourcePath._path, self.outputPath._path]

    def check_sanity(self):
        """Make sure we have a valid seeming sphinx project to work with"""
        badPaths = [path for path in self.neededPaths if not path.exists()]
        if badPaths:
            raise LoslassaError("missing paths: %s" % (badPaths))

    @cached_property
    def neededPaths(self):
        return self.neededDirPaths + [self.sphinxConfFilePath]

    @cached_property
    def neededDirPaths(self):
        return [self.projectPath, self.sourcePath]

    @cached_property
    def allPaths(self):
        return [getattr(self, p) for p in self.__dict__ if p.endswith("Path")]


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
        self.projectPath = LocalPath(projectName)

    @cli.autoswitch(str)
    def verbosity(self, level):
        """Adjust the talkativeness of loslassing activities.

        :param str level: log level (one of the accepted logging values)
        Levels from very chatty to almost silent: debug, info, warning, error
        """
        try:
            self.logLevel = logging.getLevelName(int(level))
        except ValueError:
            self.logLevel = level.upper()

    @cli.autoswitch(str)
    def log_to_file(self, filePath):
        """Log to a file instead of the console"""
        self.logFilePath = filePath

    def _init(self, create=False):
        if not self.projectPath:
            confPath = find_file(local.cwd, LoslassaProject.CONF_FILE_NAME)
            self.projectPath = confPath.dirname.up()
        self.project = LoslassaProject(self.projectPath)
        if create:
            self.project.create_empty_project()
        self.project.check_sanity()
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
            # fixme Workdir.dirname as in local.cwd.dirname crashes
            # using._path in the meantime
            # see https://github.com/tomerfiliba/plumbum/issues/78
            raise LoslassaError(
                "'%s' exists already in %s, try a different name." %
                (self.projectPath.basename, self.projectPath._path))

        self._init(create=True)


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
        log.debug("work with %s" % (self.project))
        serve_with_reloader(
            serveFromPath=str(self.project.outputPath),
            port=self.serverPort,
            changedCallback=self.project.buildCommand,
            pathToWatch=self.project.sourcePath)


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
    Loslassa.run()


if __name__ == "__main__":
    sys.exit(main())
