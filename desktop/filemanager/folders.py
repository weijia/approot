from django.http import HttpResponse
from django.core.context_processors import csrf
from django.shortcuts import render_to_response, redirect
from tagging.models import Tag, TaggedItem
#from django.core import serializers
from ui_framework.objsys.models import UfsObj, CollectionItem
import json


def root(request):
    pass
