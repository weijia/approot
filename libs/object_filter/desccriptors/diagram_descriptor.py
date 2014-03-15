from object_filter.desccriptors.obj_descriptor_base import ObjectDescriptorBase


class DiagramDescriptor(ObjectDescriptorBase):
    def get_object_action_html(self):
        #super(DiagramDescriptor, self).get_object_action_html()
        return '''
        <button class="action_button" action="/connection/start_diagram/?ufs_url=">Start</button>
        <button class="action_button" action="/connection/stop_diagram/?ufs_url=">Stop</button>
        <button class="action_button" action="/connection/auto_start/?ufs_url=">Auto start</button>
        '''

    def get_object_list_url(self):
        #super(DiagramDescriptor, self).get_object_list_url()
        return "/connection/diagram_list/"