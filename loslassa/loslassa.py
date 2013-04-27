#!/usr/bin/env python
"""The main module of loslassa as comfortable command line script"""
import logging
import os
import sys

from plumbum import cli
# noinspection PyUnresolvedReferences
from plumbum.cmd import sphinx_build
from plumbum.local_machine import LocalPath

from devserver import serve_with_reloader

log = logging.getLogger(__name__)

LOSLASSA_ROOT = os.path.abspath(os.path.dirname(__file__))
EXAMPLE_PROJECT_PATH = os.path.join(LOSLASSA_ROOT, "example_project")

__version__ = '0.3-dev-0'

class Loslassa(cli.Application):
    PROGNAME = "loslassa"
    VERSION = __version__
    verbose = cli.Flag(
        ["v", "verbose"], help = "If given, I will be very talkative")

    def main(self, *args):
        if args:
            print("unknown command %r" % (args[0]))
            return 1

        if not self.nested_command:
            print("need a command for the kind of loslassing - try --help")
            return 1

        if self.verbose:
            print "executing command %s" % str(self.nested_command)


@Loslassa.subcommand("start")
class LoslassaStart(cli.Application):
    """Starts a new project by creating the initial project structure"""

    @cli.autoswitch(str)
    def log_to_file(self, filename):
        """Sets the file into which logs will be emitted"""
        log.addHandler(logging.FileHandler(filename))


    def main(self):
        print("start loslassing...")


@Loslassa.subcommand("play")
class LoslassaPlay(cli.Application):
    """Start playing with the source and create your page"""
    serverPort = 8080
    projectPath = os.getcwd()

    @cli.autoswitch(str)
    def project_path(self, projectPath):
        """Set path instead of using CWD"""
        self.projectPath = projectPath

    @cli.autoswitch(int)
    def serve_on_port(self, port):
        """Sets the file into which logs will be emitted"""
        self.serverPort = port

    @cli.autoswitch(str)
    def log_to_file(self, filename):
        """Sets the file into which logs will be emitted"""
        log.addHandler(logging.FileHandler(filename))

    def main(self):
        """set the paths according to conventions and start serving them"""
        print("play loslassing...")
        sourcePath = LocalPath(os.path.join(self.projectPath, "source"))
        sphinxConfPath = sourcePath.join("conf.py")
        buildPath = LocalPath(os.path.join(self.projectPath, "build"))
        doctreesPath = buildPath.join("doctrees")
        outputPath = buildPath.join("html")
        self._check_paths(
            [sphinxConfPath, sourcePath, buildPath, doctreesPath, outputPath])
        sphinxBuildCommand = sphinx_build[
            "-b", "dirhtml", "-d", doctreesPath, sourcePath, outputPath]
        serve_with_reloader(
            str(outputPath), self.serverPort,
            sphinxBuildCommand,pathToWatch=str(sourcePath))

    def _check_paths(self, pathsToCheck):
        """Make sure we have a valid seeming sphinx project to work with

        :param pathsToCheck: to be checked for existence
        :type pathsToCheck: list of LocalPath
        :raise: `.LoslassaError`
        """
        for thisPath in pathsToCheck:
            if not thisPath.exists():
                raise LoslassaError(
                    "Expected path %s does not exist" % (thisPath._path))


@Loslassa.subcommand("loslassa")
class LoslassaLoslassa(cli.Application):
    """Practice loslassing by pushing your page into the interwebs"""

    def main(self):
        # todo make a progress bar consisting of loslassa :)
        print("loslassa loslassa loslassa ...")


class LoslassaError(Exception):
    pass


def main():
    logging.basicConfig(level=logging.DEBUG)
    Loslassa.run()


if __name__ == "__main__":
    # for comfy testing
    if len(sys.argv) == 1:
        sys.argv.extend(["play", "--project-path", EXAMPLE_PROJECT_PATH])
    sys.exit(main())
