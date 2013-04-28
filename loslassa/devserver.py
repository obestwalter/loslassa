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


def restart_with_reloader():
    """Spawn a new Python interpreter with the same arguments as this one,
    but running the reloader thread.
    """
    while True:
        log.info(' * Restarting with reloader')
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


def run_with_reloader(main_func, pathToWatch, interval=1):
    """Run the given function in an independent python interpreter."""
    import signal

    signal.signal(signal.SIGTERM, lambda *args: sys.exit(0))
    if os.environ.get(RUN_MAIN_ENV_KEY) == 'true':
        thread.start_new_thread(main_func, ())
        try:
            reloader_loop(pathToWatch, interval)
        except KeyboardInterrupt:
            return

    try:
        sys.exit(restart_with_reloader())
    except KeyboardInterrupt:
        pass


def reloader_loop(pathToWatch, interval=1):
    """When this function is run from the main thread, it will force other
    threads to exit when any files passed in here change..

    Copyright notice.  This function is based on ``_reloader_stat_loop()``
    from Werkzeug which is based on autoreload.py
    from CherryPy trac which originated from WSGIKit which is now dead.

    :param pathToWatch: path of the directory to be watched.
    """
    def get_watched_file_paths():
        filePaths = []
        for rootPath, _, fileNames in os.walk(pathToWatch):
            for fileName in fileNames:
                filePaths.append(os.path.join(rootPath, fileName))
        return filePaths

    pathTimeMap = {}
    while True:
        paths = get_watched_file_paths()
        shortNames = [p.rpartition(pathToWatch)[-1][1:] for p in paths]
        log.debug("check for changes: %s" % (", ".join(shortNames)))
        for filePath in paths:
            try:
                mtime = os.stat(filePath).st_mtime
            except OSError:
                continue

            oldTime = pathTimeMap.get(filePath)
            if oldTime is None:
                pathTimeMap[filePath] = mtime
                continue

            elif mtime > oldTime:
                log.info(' * Detected change in %r, reloading' % filePath)
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


def serve_with_reloader(serveFromPath, port, changedCallback, pathToWatch):
    """
    :param serveFromPath: path to the folder to be served
    :param pathToWatch: path to watch recursively for changed files
    :param port: port to be served ond
    :param changedCallback: function to be called if a monitored file changes
    """
    def call_func_then_serve():
        """Calls the passed in function and then starts the server"""
        log.info("call %s" % (changedCallback))
        changedCallback()
        server = make_server(serveFromPath, port)
        log.info("serve %s on port %s, control-C to stop" %
                 (serveFromPath, port))
        server.serve_forever()

    log.info("Serve while watching folder %s" % (pathToWatch))
    run_with_reloader(call_func_then_serve, pathToWatch)
