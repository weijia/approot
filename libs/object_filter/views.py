from django.core.context_processors import csrf
from django.shortcuts import render_to_response


# Create your views here.
from ufs_utils.django_utils import retrieve_param
from ufs_utils.string_tools import unquote_unicode


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


def get_object_table(request, descriptor_class):
    item_dict_url = descriptor_class().get_object_list_url()
    item_action_html = descriptor_class().get_object_action_html()
    c = {"user": request.user, "item_list_url": item_dict_url, "item_actions": item_action_html}
    c.update(csrf(request))
    return render_to_response('object_filter/table.html', c)





def object_table(request):
    try:
        from object_filter.desccriptors.diagram_descriptor import DiagramDescriptor
        from object_filter.desccriptors.service_descriptor import ServiceDescriptor
    except ImportError:
        pass
    descriptor_dict = {
        "diagram": DiagramDescriptor,
        "service": ServiceDescriptor,
    }

    data = retrieve_param(request)
    #item_dict_url = data.get("items_url", "/connection/diagram_list/")
    descriptor_class = descriptor_dict[data.get("descriptor", "diagram")]
    return get_object_table(request, descriptor_class)



