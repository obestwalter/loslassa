#!/usr/bin/env python
"""
========
Workflow
========

Start
=====
**not implemented yet**

::

    loslassa start */path/to/project*

Creates a new project with a basic structure and configuration
similar to sphinx-quickstart only simpler and tailored to only HTML output.

Play
====
Playing with the source and create your page. Add content and see the
changes right away thanks to local server with automatic
rebuild of the web pages::

    cd */path/to/project*
    loslassa play

Starts a local development server reachable on http://localhost:8080.
All files in project folder are being watched and if something changes
the project is rebuild.

Publish
=======
**not implemented yet**

This part is a bit vague still but basically it should simply push the
generated pages to the server, by maintaining them in a git repository

First time publishing would clone the repository bare to the web space and
set it to be origin from then on
... or summin like that, didn't think that through yet::

    cd */path/to/project*
    loslassa loslassa

Customize
=========

This is not thought out yet, but I imagine that additional customization
can be done easily by expanding the settings in the sphinx conf.py and
do more involved stuff via sphinx extensions.
"""

import logging
import os
import sys

from plumbum import cli
# noinspection PyUnresolvedReferences
from plumbum.cmd import sphinx_build
from plumbum.local_machine import LocalPath

import devserver
import utils


log = logging.getLogger("loslassa")


LOSLASSA_ROOT = os.path.abspath(os.path.dirname(__file__))
EXAMPLE_PROJECT_PATH = os.path.join(LOSLASSA_ROOT, "example_project")


__version__ = '0.3.1-dev'


class LoslassaProject(object):
    def __init__(self, projectPath):
        self.projectPath = LocalPath(projectPath)
        self.sourcePath = self.projectPath.join("source")
        self.sphinxConfPath = self.sourcePath.join("conf.py")
        self.buildPath = self.projectPath.join("build")
        self.doctreesPath = self.buildPath.join("doctrees")
        self.outputPath = self.buildPath.join("html")
        self.allPaths = [getattr(self, p) for p in self.__dict__
                         if p.endswith("Path")]

    def __str__(self):
        return utils.obj_attr(self, excludeNames=["allPaths"])

    @property
    def buildCommand(self):
        return sphinx_build[
            "-b", "dirhtml", "-d", str(self.doctreesPath),
            str(self.sourcePath), str(self.outputPath)]

    def _check_project(self):
        """Make sure we have a valid seeming sphinx project to work with

        :raise: `.LoslassaError`
        """
        for thisPath in self.allPaths:
            log.debug("check %s" % (thisPath))
            if not thisPath.exists():
                raise LoslassaError(
                    "Expected path %s does not exist" % (thisPath._path))


class LoslassaCliApplication(cli.Application):
    PROGNAME = "loslassa"
    VERSION = __version__
    USAGE = "loslassa [start|play|loslassa] [OPTIONS]"
    projectPath = None
    logLevel = logging.DEBUG
    logFilePath = None

    def __str__(self):
        return utils.obj_attr(self, excludeNames=["parent", "nested_command"])

    @cli.autoswitch(str)
    def project_name(self, projectName):
        """Set name (can be a relative or absolute path as well"""
        self.projectPath = projectName

    @cli.autoswitch(str)
    def verbosity(self, level):
        """Adjust the talkativeness of loslassing activities.

        :param str level: log level (one of the accepted logging values)
        Levels from very chatty to almost silent: debug, info, warning, error
        """
        if level.isdigit():
            self.logLevel = logging.getLevelName(int(level))
        else:
            self.logLevel = level.upper()

    @cli.autoswitch(str)
    def log_to_file(self, filePath):
        """Log to a file instead of the console"""
        self.logFilePath = filePath

    def _init(self):
        log.info("path is: %s" % (self.projectPath))
        self.project = LoslassaProject(self.projectPath)
        log.debug("project path: %s" % (self.projectPath))
        try:
            utils.init_logging(
                level=self.logLevel, filePath=self.logFilePath)
        except ValueError:
            print ("unknown verbosity level: %s use one of %s" %
                  (self.logLevel, sorted(logging._levelNames.keys())))
        log.debug("working with %s" % (self))


class Loslassa(LoslassaCliApplication):
    def main(self, *args):
        log.debug("executing command %s" % str(self.nested_command))
        if args:
            print("unknown command %r" % (args[0]))
            return 1

        if not self.nested_command:
            print("Which kind of loslassing? "
                  "Try %s --help" % (Loslassa.PROGNAME))
            return 1


@Loslassa.subcommand("start")
class LoslassaStart(LoslassaCliApplication):
    """Starts a new project by creating the initial project structure"""

    def main(self):
        log.info("start loslassing ...")
        if not self.projectPath:
            raise LoslassaError("You need to provide a name for the project")

        if os.path.exists(self.projectPath):
            raise LoslassaError("project path must not exist yet")

        self._init()
        # todo copy contents of example to project position


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
        devserver.serve_with_reloader(
            serveFromPath=str(self.project.outputPath),
            port=self.serverPort,
            changedCallback=self.project.buildCommand,
            pathToWatch=str(self.project.sourcePath))


@Loslassa.subcommand("loslassa")
class LoslassaLoslassa(LoslassaCliApplication):
    """Practice loslassing by pushing your page into the interwebs"""
    def main(self):
        self._init()
        # todo make a progress bar consisting of loslassa :)
        log.info("loslassa loslassa loslassa ...")


class LoslassaError(Exception):
    pass


def main():
    Loslassa.run()


if __name__ == "__main__":
    # for comfy testing
    if len(sys.argv) == 1:
        sys.argv.extend(["play",
                         "--verbosity", "DEBUG",
                         "--project-name", EXAMPLE_PROJECT_PATH])
    sys.exit(main())
