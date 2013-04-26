#!/usr/bin/env python
"""
To get quick feedback this implements an automatically reloading web server
to be run locally.

Reloading functionality is taken from the fabulous `Werkzeug WSGI toolkit <http://www.pocoo.org/projects/werkzeug/#werkzeug>`
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

RUN_MAIN_ENV_VAR = 'RUN_MAIN_ENV_VAR'

def restart_with_reloader():
    """Spawn a new Python interpreter with the same arguments as this one,
    but running the reloader thread.
    """
    while True:
        log.info(' * Restarting with reloader')
        args = [sys.executable] + sys.argv
        new_environ = os.environ.copy()
        new_environ[RUN_MAIN_ENV_VAR] = 'true'

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


def run_with_reloader(main_func, extra_files=None, interval=1):
    """Run the given function in an independent python interpreter."""
    import signal

    signal.signal(signal.SIGTERM, lambda *args: sys.exit(0))
    if os.environ.get(RUN_MAIN_ENV_VAR) == 'true':
        thread.start_new_thread(main_func, ())
        try:
            reloader_loop(extra_files, interval)
        except KeyboardInterrupt:
            return
    try:
        sys.exit(restart_with_reloader())
    except KeyboardInterrupt:
        pass


def reloader_loop(filesToMonitor=None, interval=1):
    """When this function is run from the main thread, it will force other
    threads to exit when any files passed in here change..

    Copyright notice.  This function is a simplified version of the
     _reloader_stat_loop from flask which is based on autoreload.py
     from CherryPy trac which originated from WSGIKit which is now dead.

    :param filesToMonitor: a list of additional files it should watch.
    """
    if not filesToMonitor:
        raise Exception("No files to watch")

    mtimes = {}
    while True:
        for filename in filesToMonitor:
            try:
                mtime = os.stat(filename).st_mtime
            except OSError:
                continue

            oldTime = mtimes.get(filename)
            if oldTime is None:
                mtimes[filename] = mtime
                continue

            elif mtime > oldTime:
                log.info(' * Detected change in %r, reloading' % filename)
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

        else:
            respond('404 Not Found', [('Content-Type', 'text/plain')])
            return ['not found']

    return simple_server.make_server('', port, minimal_wsgi_app)


def main_with_reloader(path, port, func, extraFiles=None):
    def inner():
        func()
        server = make_server(path, port)
        print("Serving {} on port {}, control-C to stop".format(path, port))
        server.serve_forever()

    run_with_reloader(inner, extra_files=extraFiles)
