import logging
import os


log = logging.getLogger(__name__)


def init_logging(level, filePath):
    """Initialize logging. If set to debug output extra info"""
    dateFmt = '%Y-%m-%d-%H:%M:%S'
    if level in ["DEBUG", 10]:
        fmt = ('%(asctime)s %(name)s %(funcName)s [%(lineno)s] %(levelname)s: '
               '%(message)s')
    else:
        fmt = '%(message)s'
    logging.basicConfig(level=level, filename=filePath,
                        format=fmt, datefmt=dateFmt)


def simple_dbg(obj, excludeNames=None):
    """pretty print information about an object

    use for quick overview while developing and for __str__ if suitable

    :param object obj: object to be print
    :param list excludeNames: list of attrs to exclude
    :rtype: str
    """
    excludeNames = excludeNames or []
    ret = ["repr: %s" % repr(obj)]
    for name in sorted([n for n in dir(obj) if n not in excludeNames]):
        try:
            attr = getattr(obj, name)
            content = str(attr).replace("\n", "\n|    ")
            ret.append("%s %s: %s" % (name, type(attr), content))
        except Exception as e:
            msg = "%s [EXC] %s '%s'" % (name, e.__class__, e.message)
            ret.append(msg)

    output = []
    for line in ret:
        if line and 'method' not in line and not line.startswith('_'):
            print line
            output.append(line)
    return os.linesep.join(output)
