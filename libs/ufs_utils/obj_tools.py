import socket

from ufs_utils import transform as transform
from logsys.logSys import *
#from objsys.models import UfsObj


def get_fs_protocol_separator():
    try:
        import configurationTools as config
        return config.getFsProtocolSeparator()
    except ImportError:
        return "://"

gUfsObjUrlPrefix = u'ufs' + get_fs_protocol_separator()
gUfsObjUrlSeparator = u'/'


log = logging.getLogger(__name__)


def is_web_url(url):
    log.error(url)
    if isUfsUrl(url):
        protocol, content = parseUrl(url)
        if protocol in ["https", "http", "ftp"]:
            return True
    return False


def get_formatted_full_path(full_path):
    return transform.format_path(full_path)


def parseUrl(url):
    return url.split(get_fs_protocol_separator(), 2)


def get_hostname():
    return unicode(socket.gethostname())


def getUfsUrl(localPath):
    return gUfsObjUrlPrefix + get_hostname() + gUfsObjUrlSeparator + transform.format_path(localPath)


def getUfsUrlForPath(fullPath):
    return getUfsUrl(fullPath)


def getFullPathFromUfsUrl(ufsUrl):
    if not isUfsFs(ufsUrl):
        raise "not ufs url"
    objPath = parseUrl(ufsUrl)[1]
    hostname, fullPath = objPath.split(gUfsObjUrlSeparator, 1)
    #print hostname, fullPath
    if unicode(hostname) != get_hostname():
        raise 'not a local file'
    return fullPath


def get_full_path_for_local_os(ufs_url):
    url_content = parseUrl(ufs_url)[1]
    if '/' == url_content[0]:
        #The path returned by qt is file:///d:/xxxx, so we must remove the '/' char first
        return url_content[1:]
    return url_content


def isUuid(url):
    return url.find(u"uuid" + get_fs_protocol_separator()) == 0


def getUrlContent(url):
    protocol, content = parseUrl(url)
    return content


def getPathForUfsUrl(url):
    url_content = getUrlContent(url)
    return url_content.split(gUfsObjUrlSeparator, 1)[1]


def getUuid(url):
    return getUrlContent(url)


def getUrlForUuid(id):
    return u"uuid" + get_fs_protocol_separator() + id


def isUfsUrl(url):
    """
    In format of xxxx://xxxx
    """
    if url.find(get_fs_protocol_separator()) == -1:
        return False
    else:
        return True


def getUfsLocalRootUrl():
    return gUfsObjUrlPrefix + get_hostname() + gUfsObjUrlSeparator


def isUfsFs(url):
    return url.find(gUfsObjUrlPrefix) == 0


def is_ufs_url(url):
    return isUfsFs(url)


def getUfsBasename(url):
    return url.rsplit(gUfsObjUrlSeparator, 1)[1]


def get_host(ufs_url):
    if isUfsFs(ufs_url):
        path_with_host = parseUrl(ufs_url)[1]
        return path_with_host.split(u"/")[0]
    raise "Not Ufs URL"


def is_local(ufs_url):
    """
    ufs_url in format ufs://hostname/D:/tmp/xxx.xxx
    """
    if get_host(ufs_url) == get_hostname():
        return True
    else:
        print "not local", get_host(ufs_url), get_hostname()
        return False