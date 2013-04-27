#!/usr/bin/env python
"""
########
Loslassa
########

A simple way to create web pages with `Python <http://python.org>`_,
`reStructuredText <http://docutils.sourceforge.net/rst.html>`_,
`git <http://git-scm.com>`_ and `love <http://en.wikipedia.org/wiki/Love>`_ :)

Other important ingredients:
    * `sphinx <http://sphinx-doc.org>`_  the documentation generator
    * simple reloading development server based on code from
      `Werkzeug  <http://www.pocoo.org/projects/werkzeug/#werkzeug>`_
    * `Plumbum <http://plumbum.readthedocs.org/en/latest/>`_ for convenient shell access
    * Permissive `BSD License <https://en.wikipedia.org/wiki/BSD_licenses>`_

============
Check it out
============

This is early days: creation and publishing functionality
does not actually exist yet ... but you can play with it already:

#. ``pip install loslassa``
#. Manually copy the example_project folder from dist-packages to your home
#. Change into example_project/source
#. ``loslassa play``
#. Point your browser to http://localhost:8080

Now you can edit the rst files or conf.py in the example project
and check the changes in the browser.

==========
Basic Idea
==========

If you want to create a simple web page without having to bother about
HTML, CSS, Javascript and all that, but don't want to suffer through those
browserbased website creatorthingies there is an alternative:
work locally with simple text files, let some clever system (sphinx) generate
the HTML and Javascript and then push the results online.

The basic workflow is inspired by the way how developing for example a
`flask <http://flask.pocoo.org/>`_ web application works: a local server runs in the
background while you edit your files and it reloads the changes as soon as they
happen. This makes it very easy to make quick changes and see the
results right away. Any errors or problems are logged to the console or are
shown right in the HTML output.

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
changes right away thanks to local server with automatic rebuild of the web pages::

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
set it to be origin from then on ... or summin like that, didn't think that through yet::

    cd */path/to/project*
    loslassa loslassa

Customize
=========

This is not thought out yet, but I imagine that additional customization
can be done easily by expanding the settings in the sphinx conf.py and
do more involved stuff via sphinx extensions.

==============
About the name
==============

**Loslassa** or **los lassa** means to let go and relax in
a german dialect called `Swabian <http://en.wikipedia.org/wiki/Swabian_German>`_
spoken in parts of South Germany. As I moved into this part of Germany in
2011 I came in direct contact with this dialect and I am still quite in
awe of it, but I really like it ... or at least I am really trying very hard to
 like it - so I thought I give my first open source project a Swabian name.

Anyway, when I came up with the idea to this project I went to my Yoga class
and my Swabian Yoga teacher always says "loslassa" whenever she wants us to
relax after some contortion she made us go through - so this is my favorite
part of the lessons.

So in the true spirit of **Loslassa** I hope this little project helps you let go of your
preconceptions how web pages have to be created and you try the Loslassa way ;).

===========
Inspiration
===========

README driven development:
    * http://tom.preston-werner.com/2010/08/23/readme-driven-development.html

Nice command line usage - heroku:
    * https://devcenter.heroku.com/articles/python
    * https://devcenter.heroku.com/articles/quickstart

Layering of functionality - git:
    * plumbing/porcelain paradigm
"""

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


__version__ = '0.4-dev'


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
            print("Which kind of loslassing? "
                  "Try %s --help"  % (Loslassa.PROGNAME))
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
