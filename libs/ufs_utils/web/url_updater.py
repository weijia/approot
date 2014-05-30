import urllib
import urlparse


def update_url_param(original_url, attr_name, attr_value):
    #Use the old url but change the offset
    parse_result = urlparse.urlparse(original_url)
    params = urlparse.parse_qs(parse_result.query)
    params[attr_name] = [attr_value]
    encoded_params = urllib.urlencode(dict((k, v if len(v) > 1 else v[0] )
                                           for k, v in params.iteritems()))
    return urlparse.urlunparse((parse_result.scheme, parse_result.netloc, parse_result.path, parse_result.params,
                                encoded_params, parse_result.fragment))


if __name__ == "__main__":
    print update_url_param("/objsys/api/ufsobj/ufsobj/?username=richard&password=richard555"
                           "password&limit=20&offset=40&format=json", "offset", "20")