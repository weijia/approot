import datetime
import logging
#noinspection PyPackageRequirements
from tagging.models import TaggedItem, Tag

log = logging.getLogger(__name__)


def get_tagged_items_greater_than_timestamp(first_tag_timestamp):
    tagged_item_filter = append_timestamp_filter_if_needed(TaggedItem.objects, first_tag_timestamp)
    return get_ordered_from_filter(tagged_item_filter)


def get_ordered_from_filter(objects_filter):
    tagged_item_list = objects_filter.order_by('timestamp')
    return tagged_item_list


def append_timestamp_filter_if_needed(certain_tagged_item_filter, first_tag_timestamp):
    if 0 == first_tag_timestamp:
        log.debug('timestamp is zero')
    else:
        django_time = datetime.datetime.fromtimestamp(first_tag_timestamp).replace(tzinfo=utc)
        log.debug("timestamp", django_time, first_tag_timestamp)
        certain_tagged_item_filter.filter(timestamp__gt=django_time)
    return certain_tagged_item_filter


def get_items_with_certain_tag_greater_than_timestamp(first_tag_timestamp, tag_name):
    tag = Tag.objects.get(name=tag_name)
    certain_tagged_item_filter = TaggedItem.objects.filter(tag__exact=tag.pk)
    append_timestamp_filter_if_needed(certain_tagged_item_filter, first_tag_timestamp)
    tagged_item_list = get_ordered_from_filter(certain_tagged_item_filter)
    return tagged_item_list