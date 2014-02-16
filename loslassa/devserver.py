#!/usr/bin/env python
"""
To get quick feedback this implements an automatically reloading web server
to be run locally.

Reloading functionality is taken from the fabulous
`Werkzeug WSGI toolkit <http://www.pocoo.org/projects/werkzeug/#werkzeug>`
"""
import logging
import mimetypes
import os
import subprocess
import sys
import time
import thread
from wsgiref import simple_server, util


log = logging.getLogger(__name__)


RUN_MAIN_ENV_KEY = 'RUN_MAIN_ENV_KEY'


# todo refactor into generalized class
# todo use local.path object throughout


def restart_with_reloader():
    """Spawn a new Python interpreter with the same arguments as this one,
    but running the reloader thread.
    """
    while True:
        log.info("***restarting with reloader***")
        args = [sys.executable] + sys.argv
        new_environ = os.environ.copy()
        new_environ[RUN_MAIN_ENV_KEY] = 'true'
        # a weird bug on windows. sometimes unicode strings end up in the
        # environment and subprocess.call does not like this, encode them
        # to latin1 and continue.
        if os.name == 'nt':
            for key, value in new_environ.iteritems():
                if isinstance(value, unicode):
                    new_environ[key] = value.encode('iso-8859-1')
        exit_code = subprocess.call(args, env=new_environ)
        if exit_code != 3:
            return exit_code


def run_with_reloader(main_func, pathToWatch, pathToIgnore,
                      cleanFileNames, cleanPaths):
    """Run the given function in an independent python interpreter."""
    import signal

    signal.signal(signal.SIGTERM, lambda *args: sys.exit(0))
    if os.environ.get(RUN_MAIN_ENV_KEY) == 'true':
        thread.start_new_thread(main_func, ())
        try:
            reloader_loop(pathToWatch, pathToIgnore,
                          cleanFileNames, cleanPaths)
        except KeyboardInterrupt:
            return

    try:
        sys.exit(restart_with_reloader())
    except KeyboardInterrupt:
        pass


def reloader_loop(pathToWatch, pathToIgnore, cleanFileNames, cleanPaths,
                  interval=0.5):
    """When this function is run from the main thread, it will force other
    threads to exit when any files passed in here change..

    Copyright notice: this function is based on ``_reloader_stat_loop()``
    from Werkzeug which is based on autoreload.py
    from CherryPy trac which originated from WSGIKit which is now dead.

    :param LocalPath pathToWatch: path of the directory to be watched.
    """
    pathTimeMap = {}
    while True:
        paths = [p for p in pathToWatch.walk(
            filter=lambda _: "\\." not in p._path and "/." not in p._path)
            if not p._path.startswith(pathToIgnore._path) and
            "\\." not in p._path and "/." not in p._path and not
            p.isdir()]
        changedPaths = []
        for filePath in paths:
            try:
                mtime = filePath.stat().st_mtime
            except OSError:
                log.warning("problem with %s" % (filePath), exc_info=True)
                continue

            oldTime = pathTimeMap.get(filePath)
            if oldTime is None:
                pathTimeMap[filePath] = mtime
                continue

            elif mtime > oldTime:
                changedPaths.append(filePath.basename)
                if cleanFileNames == "ALL":
                    break

        if changedPaths:
            # fixme handle changes in build dir intelligently (query git)
            log.info("detected changes in %s: reloading" % (changedPaths))
            if (cleanFileNames == "ALL" or
                    any(n in [b.basename for b in changedPaths]
                        for n in cleanFileNames)):
                log.info("cleaning necessary in %s" % (cleanPaths))
                for path in cleanPaths:
                    log.info("cleaning %s" % (path))
                    path.delete()
            log.info("reloading ...")
            sys.exit(3)

        time.sleep(interval)


def make_server(path, port):
    def minimal_wsgi_app(environ, respond):
        """simple wsgi app to serve html files"""
        fn = os.path.join(path, environ['PATH_INFO'][1:])
        if '.' not in fn.split(os.path.sep)[-1]:
            fn = os.path.join(fn, 'index.html')
        type_ = mimetypes.guess_type(fn)[0]
        if os.path.exists(fn):
            respond('200 OK', [('Content-Type', type_)])
            return util.FileWrapper(open(fn, "rb"))

        respond('404 Not Found', [('Content-Type', 'text/plain')])
        return ['404 not found']

    return simple_server.make_server('', port, minimal_wsgi_app)


def serve_with_reloader(
        serveFromPath, port, changedCallback, pathToWatch, pathToIgnore,
        cleanFileNames=None, cleanPaths=None):
    """

    :param serveFromPath: path to the folder to be served
    :param pathToWatch: path to watch recursively for changed files
    :param port: port to be served ond
    :param changedCallback: function to be called if a monitored file changes
    :param pathToIgnore: don't watch this path for changes
    :param cleanFileNames: list of filenames that should trigger a full clean
    :param cleanPaths: paths to delete on a full clean
    """
    def call_func_then_serve():
        """Calls the passed in function and then starts the server"""
        result = changedCallback()
        log.info("call %s -> %s" % (changedCallback.__name__, result))
        server = make_server(serveFromPath._path, port)
        log.info("serve %s on http://localhost:%s, control-C to stop" %
                 (serveFromPath, port))
        server.serve_forever()

    log.info("Serve while watching folder %s" % (pathToWatch))
    run_with_reloader(call_func_then_serve, pathToWatch, pathToIgnore,
                      cleanFileNames or [], cleanPaths or [])
