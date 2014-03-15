from object_filter.desccriptors.obj_descriptor_base import ObjectDescriptorBase


class ServiceDescriptor(ObjectDescriptorBase):
    def get_object_list_url(self):
        #super(ServiceDescriptor, self).get_object_list_url()
        return "/connection/services_list_tastypie_format/"

    def get_object_action_html(self):
        #super(ServiceDescriptor, self).get_object_action_html()
        return '''
        <button class="action_button" action="/obj_operation/service/start/?ufs_url=">Start</button>
        <button class="action_button" action="/obj_operation/service/stop/?ufs_url=">Stop</button>
        <button class="action_button" action="/connection/auto_start/?ufs_url=">Auto start</button>
        '''