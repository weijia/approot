import urllib2


def open_url(full_web_url):
    proxy_handler = urllib2.ProxyHandler({})
    opener = urllib2.build_opener(proxy_handler)
    opener.open(full_web_url)