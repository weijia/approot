from django.conf.urls.defaults import *
from jsonrpc import jsonrpc_site
import json_rpc_for_obj_importer # you must import the views that need connected

urlpatterns = patterns('', 
  url(r'^json/browse/', 'jsonrpc.views.browse', name="jsonrpc_browser"), # for the graphical browser/web console only, omissible
  url(r'^json/', jsonrpc_site.dispatch, name="jsonrpc_mountpoint"),
  (r'^json/(?P<method>[a-zA-Z0-9.]+)$', jsonrpc_site.dispatch) # for HTTP GET only, also omissible
)