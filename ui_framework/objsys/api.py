from tastypie.resources import ModelResource
from libs.utils.django_utils import retrieve_param
from models import UfsObj
from tastypie.authentication import SessionAuthentication
from tastypie.authentication import Authentication
from tastypie.authorization import DjangoAuthorization
#from django.contrib.auth.models import User, Group
from tagging.models import Tag
from tagging.models import TaggedItem
from django.contrib.auth import authenticate, login


class DjangoUserAuthentication(Authentication):
    def is_authenticated(self, request, **kwargs):
        data = retrieve_param(request)
        if not request.user.is_authenticated():
            username = data['username']
            password = data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return True
        else:
            return True
        return False

    # Optional but recommended
    def get_identifier(self, request):
        return request.user.username


class UfsObjResource(ModelResource):
    #json_indent = 2

    def get_object_list(self, request):
        #return super(UfsObjResource, self).get_object_list(request).filter(start_date__gte=now)
        data = retrieve_param(request)
        tag = None
        if "tag" in request.session:
            if "offset" in data:
                tag = request.session["tag"]
            else:
                #Do not have offset means it may be a new serial of object query
                del request.session["tag"]

        if "tag" in data:
            tag = data["tag"]

        if tag is None:
            return super(UfsObjResource, self).get_object_list(request)
        else:
            request.session["tag"] = tag
            try:
                obj_tag = Tag.objects.get(name=tag)
                objs = TaggedItem.objects.get_by_model(UfsObj, obj_tag).order_by('-timestamp')
            except:
                objs = UfsObj.objects.none()
            return objs


    def dehydrate(self, bundle):
        res = []
        for tag in bundle.obj.tags:
            res.append(tag)
        bundle.data["tags"] = res
        return bundle

    '''
    def build_filters(self, filters=None):
        if filters is None:
            filters = {}

        orm_filters = super(MyResource, self).build_filters(filters)

        if "tag" in filters:
            sqs = SearchQuerySet().auto_query(filters['q'])

            orm_filters["pk__in"] = [i.pk for i in sqs]

        return orm_filters
    '''

    class Meta:
        queryset = UfsObj.objects.all().order_by("timestamp")
        resource_name = 'ufsobj'
        #authentication = SessionAuthentication()
        authentication = DjangoUserAuthentication()
        authorization = DjangoAuthorization()
        filtering = {
            "ufs_url": ('contains',),
            "full_path": ('contains', 'iendswith'),
        }


'''
class TagResource(ModelResource):
    class Meta:
        queryset = Tag.objects.usage_for_model(UfsObj)
        resource_name = 'tag'
        #authentication = SessionAuthentication()
        authentication = DjangoUserAuthentication()
        authorization = DjangoAuthorization()
'''

'''
class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        resource_name = 'user'
        #authentication = SessionAuthentication()
        authentication = DjangoUserAuthentication()
        authorization = DjangoAuthorization()
        excludes = ['email', 'password', 'is_staff', 'is_superuser']
        filtering = {
            "username": ('exact', 'startswith',),
        }
        
class GroupResource(ModelResource):
    class Meta:
        queryset = Group.objects.all()
        resource_name = 'group'
        #authentication = SessionAuthentication()
        authentication = DjangoUserAuthentication()
        authorization = DjangoAuthorization()
'''