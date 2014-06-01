import logging
import urllib
import urlparse


log = logging.getLogger(__name__)


def update_url_param(original_url, attr_name, attr_value):
    #Use the old url but change the offset
    log.error("%s, %s, %s" % (str(original_url), str(attr_name), str(attr_value)))
    parse_result = urlparse.urlparse(original_url)
    params = urlparse.parse_qs(parse_result.query)
    params[attr_name] = [attr_value]
    encoded_params = urllib.urlencode(dict((k, v if len(v) > 1 else v[0] )
                                           for k, v in params.iteritems()))
    return urlparse.urlunparse((parse_result.scheme, parse_result.netloc, parse_result.path, parse_result.params,
                                encoded_params, parse_result.fragment))


def get_server_base(url):
    parse_result = urlparse.urlparse(url)
    return urlparse.urlunparse((parse_result.scheme, parse_result.netloc, "", "", "", ""))


if __name__ == "__main__":
    print update_url_param("/objsys/api/ufsobj/ufsobj/?username=richard&password=richard555"
                           "password&limit=20&offset=40&format=json", "offset", "20")


    print get_server_base("http://127.0.0.1:8110/url_based_task_apps/export/1/?processor_uuid=b2c1bd6f-5f9a-4093-b842-250b8aa30b06&initial_import_url=http://allbookmarks.sinaapp.com/objsys/api/ufsobj/ufsobj/?format=json%26username=richard%26password=richard555password")