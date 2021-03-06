import logging
import time
from msg_service.predefined_receivers import DISTRIBUTOR
from services.svc_base.stated_worker import StatedWorker
from tags.tag_utils import get_items_with_certain_tag_greater_than_timestamp
from services.sap.msg_service_sap import AutoRouteMsgService


log = logging.getLogger(__name__)


class CertainTaggedItemEnumWorker(StatedWorker):
    def __init__(self, diagram_info, parent, group=None, target=None, name=None, args=(), kwargs=None, verbose=None):
        processor_uuid = diagram_info["processor_uuid"]
        super(CertainTaggedItemEnumWorker, self).__init__(processor_uuid, parent, group, target, name, args, kwargs,
                                                          verbose)
        self.diagram_info = diagram_info

    def run(self):
        #Retrieve saved last timestamp, will start to enumerate items with greater (not equal) timestamp
        first_tag_timestamp = self.state.get_state_value("certain_tag_enum_start_timestamp", 0)
        log.debug("first tag timestamp:" + str(first_tag_timestamp))

        tag = self.state.get_state_value("tag", "git_repo")

        tagged_item_list = get_items_with_certain_tag_greater_than_timestamp(
            first_tag_timestamp, tag)

        #Send all retrieved items
        for tagged_item in tagged_item_list:

            obj_tag = tagged_item.tag.name
            obj = tagged_item.object
            tag_app = tagged_item.tag_app

            log.debug("got tag", obj, tagged_item.timestamp, first_tag_timestamp, time.mktime(
                tagged_item.timestamp.timetuple()) + (tagged_item.timestamp.microsecond / 1000000.0))
            AutoRouteMsgService().send_to(DISTRIBUTOR, {
                "diagram": self.diagram_info,
                "ufs_url": obj.ufs_url,
                "uuid": obj.uuid, "full_path": obj.full_path, "tag": obj_tag,
                "tag_app": tag_app,
                "timestamp": time.mktime(tagged_item.timestamp.timetuple()) +
                (tagged_item.timestamp.microsecond / 1000000.0),
                "diagram_id": self.diagram_info["diagram_id"]})
            if self.is_quitting():
                break
            time.sleep(1)
