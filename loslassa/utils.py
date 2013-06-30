import logging
import traceback

from plumbum.local_machine import local


log = logging.getLogger()


def adjust_log_formatter(level, filePath):
    """Add file handler to logging. If set to debug output extra info

    :param level: log level (one of the logging level constants)
    :param filePath: path to where the logfile should be written to
    """
    fmt = '%(message)s'
    dateFmt = '%Y-%m-%d-%H:%M:%S'
    if log.getEffectiveLevel() <= logging.DEBUG:
        fmt = ('%(asctime)s %(funcName)s [%(lineno)s] %(levelname)s: ' + fmt)
    formatter = logging.Formatter(fmt=fmt, datefmt=dateFmt)
    if filePath:
        log.addHandler(logging.FileHandler(filePath))
    for handler in log.handlers:
        handler.setFormatter(formatter)


def simple_dbg(obj, excludeNames=None):
    """pretty print information about an object

    use for quick overview while developing and for __str__ if suitable

    :param object obj: object to be print
    :param list excludeNames: list of attrs to exclude
    :rtype: str
    """
    excludeNames = excludeNames or []
    lines = ["%s" % repr(obj)]
    for name in sorted([n for n in dir(obj) if n not in excludeNames]):
        try:
            attr = getattr(obj, name)
            content = str(attr).replace("\n", "\n|    ")
            lines.append("%s %s: %s" % (name, type(attr), content))
        except Exception as e:
            msg = "[EXC]%s: %s: %s" % (name, e.__class__.__name__, e.message)
            lines.append(msg)
    return "\n".join(
        [line for line in lines
         if line and 'method' not in line and not line.startswith('_')])


def find_file(searchPath, wantedName):
    with local.cwd(searchPath):
        matches = [p for p in local.cwd.walk() if p.basename == wantedName]
    if len(matches) == 1:
        return matches[0]

    if not matches:
        raise UtilsError("%s not found in %s" % (wantedName, searchPath))

    raise UtilsError(
        "too many projects found in %s: %s" % (searchPath, matches))


def friendly_exception_handler(exception_type, exception, tb):
    if isinstance(exception_type, LoslassaError):
        msg = exception.message
    else:
        msg = (
            "Whoops that was uncalled for ... sorry about that :(\n"
            "An error of %s occurred.\n"
            "The error message was '%s'" % (exception_type, exception))
    rbString = ''.join(traceback.format_tb(tb))
    msg += (
        "What follows might not say much to you, but somebody who knows "
        "Python will be able to figure out what went wrong:\n%s" % (rbString))
    log.error(msg)


class cached_property(object):
    """read-only property that's only evaluated once (filched from Werkzeug)"""
    def __init__(self, fget, doc=None):
        self.fget = fget
        self.__doc__ = doc or fget.__doc__
        self.__name__ = fget.__name__

    def __get__(self, obj, _):
        if obj is None:
            return self

        obj.__dict__[self.__name__] = result = self.fget(obj)
        return result


class LoslassaError(Exception):
    pass


class UtilsError(LoslassaError):
    pass
