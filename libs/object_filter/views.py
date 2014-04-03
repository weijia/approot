from django.core.context_processors import csrf
from django.shortcuts import render_to_response


# Create your views here.
from utils.django_utils import retrieve_param
from utils.string_tools import unquote_unicode


def object_filter(request):
    data = retrieve_param(request)

    c = {"user": request.user}
    if "tag" in data:
        c["tag"] = data["tag"]
        c["filter_tag"] = True

    if "query_base" in data:
        c["query_base"] = unquote_unicode(data["query_base"])
        c["query_base_exists"] = True
    try:
        import configuration
        thumb_server_port = configuration.g_config_dict.get("thumb_server_port", 8114)
        c["thumb_server_base"] = "http://%s:%d/thumb/cherry/" % (request.META['HTTP_HOST'].split(":")[0], thumb_server_port)
    except:
        c["thumb_server_base"] = "/static/img/icons/16px/html.png"

    c.update(csrf(request))
    return render_to_response('object_filter/index.html', c)


def object_table(request):
    data = retrieve_param(request)

    c = {"user": request.user}
    '''
    if "tag" in data:
        c["tag"] = data["tag"]
        c["filter_tag"] = True

    if "query_base" in data:
        c["query_base"] = string_tools.unquote_unicode(data["query_base"])
        c["query_base_exists"] = True
    '''
    c.update(csrf(request))
    return render_to_response('object_filter/table.html', c)