import logging
import os


log = logging.getLogger(__name__)


def init_logging(level, filePath):
    """Intialize logging. If set to debug output extra info"""
    dateFmt = '%Y-%m-%d-%H:%M:%S'
    if level in ["DEBUG", 10]:
        fmt = ('%(asctime)s %(name)s %(funcName)s [%(lineno)s] %(levelname)s: '
               '%(message)s')
    else:
        fmt = '%(message)s'
    logging.basicConfig(level=level, filename=filePath,
                        format=fmt, datefmt=dateFmt)


def obj_attr(obj, hideString='', filterMethods=True, filterPrivate=True,
             excludeNames=None, indent=0):
    """pretty print information about an object

    use for quick overview while developing and for __str__ if suitable

    :param object obj: object to be print
    :param bool filterMethods: don't show object methods
    :param bool filterPrivate: don't show private attributes and methods
    :param list excludeNames: list of attrs to exclude
    :param str hideString: if attr contains string - don't show
    :param int indent: indent the output
    :rtype: str
    """
    excludeNames = excludeNames or []
    out = ["repr: %s" % repr(obj)]
    try:
        out += ["__dict__: %s" % (obj.__dict__)]
    except Exception:
        pass

    for name in sorted([n for n in dir(obj) if n not in excludeNames]):
        try:
            attr = getattr(obj, name)
            content = str(attr).replace("\n", "\n|    ")
            out.append("%s %s: %s" % (name, type(attr), content))
        except Exception as e:
            msg = "%s [EXCEPTION] %s '%s'" % (name, e.__class__, e.message)
            out.append(msg)

    if hideString:
        out = [l for l in out if hideString not in l]

    if filterPrivate:
        out = [l for l in out if not l.startswith('_')]

    if filterMethods:
        out = [line for line in out
               if line and
               'method' not in line and
               '__dict__' not in line
               and '__doc__' not in line]

    out = (
        ["%s (%s)" % (type(obj), (id(obj)))] +
        ["," + "-" * 80] +
        ["| %s" % (line) for line in out] +
        ["'" + "-" * 80])
    if indent:
        out = ["%s%s" % (" " * indent, o) for o in out]
    return os.linesep.join(out)
