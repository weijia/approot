from django.db import models
from django.utils.translation import ugettext_lazy
from objsys.models import UfsObj, get_new_uuid

class Connection(models.Model):
    '''
    * Just used because Processor may contain several inputs or outputs, there must be an model so we can use many to many pattern
    '''
    connection_uuid = models.CharField(max_length=60, default=get_new_uuid)
    def __unicode__(self):
        return unicode(self.connection_uuid)

# Create your models here.
class Processor(models.Model):
    '''
    * Processor design
    
        Create diagram:
        

    * Start diagram
    
        for processor in diagram:
            if processor is diagram:
                start diagram(processor.params)
            else:
                start processor(processor.params)
                
                
    * Start processor:
    
        processor.input
        processor.output
        processor.params
    '''
    #Object for the script or the diagram
    ufsobj = models.ForeignKey(UfsObj)
    
    diagram_obj = models.ForeignKey(UfsObj, related_name="diagram_obj")
    #{"tag": "Tag name", "target": "Target tube name"}
    #The above param will be translated to the following and pass to the processor command line
    #--tag "nsn" --target "archiver-xxxx-yyyyy-aaaa-bbbb-cccc-pppp"
    #target is used by system to put the generated items into this specific target tube name
    param_descriptor = models.CharField (ugettext_lazy(u"param_descriptor"),
                                            help_text=ugettext_lazy(u"description of the processor's param"),
                                            max_length=500, null=True, blank=True)
    created = models.DateTimeField('date published', auto_now_add = True)
    
    #There might be several inputs and outputs
    inputs = models.ManyToManyField(Connection, related_name="inputs", null=True, blank=True)
    outputs = models.ManyToManyField(Connection, related_name="outputs", null=True, blank=True)
    

    def __unicode__(self):
        return unicode(self.ufsobj.ufs_url) + u'->' + unicode(self.diagram_obj.ufs_url)


        

