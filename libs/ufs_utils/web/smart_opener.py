import urllib2


def open_url(full_web_url):
    try:
        proxy_handler = urllib2.ProxyHandler({})
        opener = urllib2.build_opener(proxy_handler)
        return opener.open(full_web_url)
    except KeyError:
        return urllib2.urlopen(full_web_url)