import logging
import random
from django.contrib.auth.models import User
from tagging.models import Tag
from objsys.models import UfsObj, Description
from objsys.tastypie_related.tasypie_item import TastypieItem


log = logging.getLogger(__name__)


class TastypieImporter(object):
    def __init__(self):
        super(TastypieImporter, self).__init__()
        self.log_str = ""
        self.added_list = []
        self.seed = random.randint(0,10000)

    def is_already_exist(self, tastypie_item):
        if 0 == UfsObj.objects.filter(ufs_url=tastypie_item.get_url()).count():
            log.error("%d. not exist: %s" % (self.seed, tastypie_item.get_url()))
            return False
        return True

    def import_one_obj(self, item, user_id=1):
        tastypie_item = TastypieItem(item)
        #user_id = self.kwargs['user_id']
        user = User.objects.get(pk=user_id)
        if tastypie_item.is_valid_url() and (not self.is_already_exist(tastypie_item)):
            if not (tastypie_item.get_url() in self.added_list):
                self.added_list.append(tastypie_item.get_url())
            else:
                log.error("%d, %s already added" % (self.seed, tastypie_item.get_url()))
                return

            tags_str = tastypie_item.get_tag_str()
            del item["tags"]
            description = tastypie_item.get_description_content()
            del item["descriptions"]
            del item["resource_uri"]
            del item["id"]
            obj, created = UfsObj.objects.get_or_create(user=user, **item)
            if not (obj.pk is None):
                log.error("first: seed: %d, pk: %d, url: %s" % (self.seed, obj.pk, obj.ufs_url))
            if description != "":
                description_obj, created = Description.objects.get_or_create(content=description)
                obj.descriptions.add(description_obj)
                obj.save()
                log.error("second: seed: %d, pk: %d, url: %s" % (self.seed, obj.pk, obj.ufs_url))
            Tag.objects.update_tags(obj, tags_str, tag_app='import from BAE')
            self.log_str += tastypie_item.get_url() + "Tag:" + tags_str + "\n"
        else:
            self.log_str += "ignored:" + tastypie_item.get_url() + "\nis valid:" + str(
                tastypie_item.is_valid_url()) + "\n"

    def import_data_from_tastypie_result(self, decoded, user_id=1):
        #decoded = json.loads(result)
        for item in decoded["objects"]:
            #tastypie_item = TastypieItem(item)
            try:
                self.import_one_obj(item, user_id)
            except:
                import traceback
                log.error(traceback.format_exc())
        #log.error(self.log_str)