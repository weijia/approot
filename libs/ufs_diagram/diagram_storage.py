from objsys.models import UfsObj


class DiagramStorage(object):
    @staticmethod
    def rm_diagram(diagram_uuid):
        #Processors will be automatically deleted according to django queryset.delete method.
        UfsObj.objects.filter(ufs_url=u"diagram://" + diagram_uuid, valid=True).delete()
