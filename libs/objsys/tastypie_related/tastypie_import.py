import logging
from django.contrib.auth.models import User
from tagging.models import Tag
from objsys.models import UfsObj, Description
from objsys.tastypie_related.tasypie_item import TastypieItem


log = logging.getLogger(__name__)


class TastypieImporter(object):
    def __init__(self):
        super(TastypieImporter, self).__init__()
        self.log_str = ""

    @staticmethod
    def is_already_exist(tastypie_item):
        if 0 == UfsObj.objects.filter(ufs_url=tastypie_item.get_url()).count():
            log.error("already exist:"+tastypie_item.get_url())
            return True
        return False

    def import_one_obj(self, item, user_id=1):
        tastypie_item = TastypieItem(item)
        if tastypie_item.is_valid_url() and self.is_already_exist(tastypie_item):
            #user_id = self.kwargs['user_id']
            user = User.objects.get(pk=user_id)
            tags_str = tastypie_item.get_tag_str()
            del item["tags"]
            description = tastypie_item.get_description_content()

            del item["descriptions"]
            del item["resource_uri"]
            del item["id"]
            obj = UfsObj(user=user, **item)
            obj.save()
            if description != "":
                description_obj, created = Description.objects.get_or_create(content=description)
                obj.descriptions.add(description_obj)
                obj.save()
            Tag.objects.update_tags(obj, tags_str, tag_app='import from BAE')
            self.log_str += tastypie_item.get_url() + "Tag:" + tags_str + "\n"
        else:
            self.log_str += "ignored:" + tastypie_item.get_url() + "\nis valid:" + str(
                tastypie_item.is_valid_url()) + "\n"

    def import_data_from_tastypie_result(self, decoded, user_id=1):
        #decoded = json.loads(result)
        for item in decoded["objects"]:
            #tastypie_item = TastypieItem(item)
            self.import_one_obj(item, user_id)
        log.error(self.log_str)