import logging
from ufs_utils.obj_tools import is_web_url, is_ufs_url

log = logging.getLogger(__name__)


class TastypieItem(object):
    def __init__(self, tastypie_item_dict):
        super(TastypieItem, self).__init__()
        self.item = tastypie_item_dict

    def is_valid_url(self):
        url = self.get_url()
        log.debug(url)
        if url == "":
            return False
        if is_web_url(url):
            return True
        if is_ufs_url(url):
            return True
        return False

    def get_description(self):
        descriptions = self.item["descriptions"]
        if len(descriptions) > 0:
            description = descriptions[0]
        else:
            description = ""
        return description

    def get_description_content(self):
        description = self.get_description()
        result = ""
        if "content" in description:
            result = description["content"]
        return result

    def get_url(self):
        url = self.item["ufs_url"]
        return url

    def get_tag_str(self):
        tags = self.item["tags"]

        if len(tags) > 0:
            tags_str = u",".join(tags)
        else:
            tags_str = ""
        return tags_str