import socket
import configurationTools as config
from libs.obj_related.json_obj import JsonDecoderForUfsObj
from libs.utils import transform as transform
from libs.logsys.logSys import *
from objsys.models import UfsObj


gUfsObjUrlPrefix = u'ufs'+config.getFsProtocolSeparator()
gUfsObjUrlSeparator = u'/'


def is_web_url(url):
    protocol, content = parseUrl(url)
    if protocol in ["https", "http", "ftp"]:
        return True
    return False


def get_formatted_full_path(full_path):
    return transform.transformDirToInternal(full_path)


def parseUrl(url):
    return url.split(config.getFsProtocolSeparator(),2)
    

def getHostName():
    return unicode(socket.gethostname())


def getUfsUrl(localPath):
    return gUfsObjUrlPrefix+getHostName()+gUfsObjUrlSeparator+transform.transformDirToInternal(localPath)


def getUfsUrlForPath(fullPath):
    return getUfsUrl(fullPath)


def getFullPathFromUfsUrl(ufsUrl):
    if not isUfsFs(ufsUrl):
        cl(ufsUrl)
        raise "not ufs url"
    objPath = parseUrl(ufsUrl)[1]
    hostname, fullPath = objPath.split(gUfsObjUrlSeparator, 1)
    #print hostname, fullPath
    if unicode(hostname) != getHostName():
        raise 'not a local file'
    return fullPath


def get_full_path_for_local_os(ufs_url):
    url_content = parseUrl(ufs_url)[1]
    if '/' == url_content[0]:
        #The path returned by qt is file:///d:/xxxx, so we must remove the '/' char first
        return url_content[1:]
    return url_content


def isUuid(url):
    return url.find(u"uuid"+config.getFsProtocolSeparator()) == 0


def getUrlContent(url):
    protocol, content = parseUrl(url)
    return content


def getPathForUfsUrl(url):
    url_content = getUrlContent(url)
    return url_content.split(gUfsObjUrlSeparator, 1)[1]


def getUuid(url):
    return getUrlContent(url)


def getUrlForUuid(id):
    return u"uuid"+config.getFsProtocolSeparator()+id


def isUfsUrl(url):
    """
    In format of xxxx://xxxx
    """
    if url.find(config.getFsProtocolSeparator()) == -1:
        return False
    else:
        return True


def getUfsLocalRootUrl():
    return gUfsObjUrlPrefix+getHostName()+gUfsObjUrlSeparator


def isUfsFs(url):
    return url.find(gUfsObjUrlPrefix) == 0


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
    if get_host(ufs_url) == getHostName():
        return True
    else:
        print "not local", get_host(ufs_url), getHostName()
        return False


def get_ufs_obj_from_ufs_url(ufs_url):
    obj_list = UfsObj.objects.filter(ufs_url=ufs_url)
    if 0 == obj_list.count():
        obj = UfsObj(ufs_url=ufs_url)
        obj.save()
    else:
        obj = obj_list[0]
    return obj


def get_ufs_obj_from_full_path(full_path):
    full_path = transform.transformDirToInternal(full_path)
    obj_list = UfsObj.objects.filter(full_path=full_path)
    if 0 == obj_list.count():
        ufs_url = getUfsUrlForPath(full_path)
        obj = UfsObj(ufs_url=ufs_url, full_path=full_path)
        obj.save()
    else:
        obj = obj_list[0]
    return obj


def get_or_create_ufs_obj_from_path_and_url(full_path, ufs_url):
    """
    full_path and ufs_url must not be empty (""), will be checked here
    """
    if ("" == full_path) or ("" == ufs_url):
        print "Invalid parameter:", full_path, ufs_url
        raise "Invalid parameter"
    if 0 == UfsObj.objects.filter(full_path=full_path, valid=True).count():
        return UfsObj.objects.get_or_create(ufs_url=ufs_url, valid=True)

    for ufs_obj in UfsObj.objects.filter(full_path, valid=True):
        if ufs_obj.ufs_url == ufs_url:
            return ufs_obj, False
        else:
            print "UFS Url not match while full path is equal", full_path, ufs_url, ufs_obj.ufs_url
            raise "UFS Url not match while full path is equal"


def get_ufs_obj_from_json(json_dict):
    decoded_obj = JsonDecoderForUfsObj(json_dict)
    if decoded_obj.is_full_path_valid() and decoded_obj.is_ufs_url_valid():
        ufs_obj, created = get_or_create_ufs_obj_from_path_and_url(decoded_obj.get_full_path(),
                                                                       decoded_obj.get_ufs_url())
    elif (not decoded_obj.is_ufs_url_valid()) and (not decoded_obj.is_full_path_valid()):
        print "Invalid json dict:", json_dict
        raise "Invalid json dict"
    else:
        ufs_obj, created = UfsObj.objects.get_or_create(**decoded_obj.get_ufs_obj_attribute_dict(), valid=True)
    return ufs_obj