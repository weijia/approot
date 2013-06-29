# -*- coding: utf-8 -*-  
from django.db import models
from django.utils.translation import ugettext_lazy

# Create your models here.
class Processor(models.Model):
    '''
    StudentID = models.IntegerField (ugettext_lazy(u"学员编号"),help_text=ugettext_lazy(u" 学员编号。 ") , default=0 )# 学员编号。
    StudentName = models.CharField (ugettext_lazy(u"学员姓名"),help_text=ugettext_lazy(u" 学员姓名。 ") , max_length=50 )# 学员姓名。
    PYSimple = models.CharField (ugettext_lazy(u"拼音简码"),help_text=ugettext_lazy(u" 拼音简码。 ") , max_length=50 )# 拼音简码。
    Byname = models.CharField (ugettext_lazy(u"别名"),help_text=ugettext_lazy(u" 别名。 ") , max_length=50 )# 别名。
    Appellation = models.CharField (ugettext_lazy(u"称呼"),help_text=ugettext_lazy(u" 称呼。 ") , max_length=50 )# 称呼。
    SEX_CHOICES = (
        (0, u"女"),
        (1, u"男"),
    )
    '''
    processor_full_path = models.CharField (ugettext_lazy(u"processor_full_path"),help_text=ugettext_lazy(u"full path of the processor") , max_length=500)
    output_name = models.CharField (ugettext_lazy(u"output_name"),help_text=ugettext_lazy(u"output of the processor") , max_length=500)
    created = models.DateTimeField('date published')
    #{"tag": "Tag name", "target": "Target tube name"}
    #The above param will be translated to the following and pass to the processor command line
    #--tag "nsn" --target "archiver-xxxx-yyyyy-aaaa-bbbb-cccc-pppp"
    #target is used by system to put the generated items into this specific target tube name
    param_descriptor = models.CharField (ugettext_lazy(u"param_descriptor"),help_text=ugettext_lazy(u"description of the processor's param") , max_length=500)
    
class ProcessWorkflow(models.Model):
    created = models.DateTimeField('date published')
    
    
class ProcessorInstance(models.Model):
    workflow = models.ForeignKey(ProcessWorkflow)
    processor = models.ForeignKey(Processor)
    param = models.CharField (ugettext_lazy(u"param_descriptor"),help_text=ugettext_lazy(u"description of the processor's param") , max_length=500)
    next_processor_instance = models.ForeignKey('self')
    
