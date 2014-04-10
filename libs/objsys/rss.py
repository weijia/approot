from django.contrib.syndication.views import Feed
from django.core.urlresolvers import reverse
from objsys.models import UfsObj


class LatestEntriesFeed(Feed):
    title = "My bookmarks"
    link = "/sitenews/"
    description = "Updates on changes and additions to police beat central."

    def items(self):
        return UfsObj.objects.order_by('-timestamp')

    def item_title(self, item):
        try:
            return item.descriptions.all()[0].content
        except IndexError:
            return ""

    def item_description(self, item):
        try:
            return item.descriptions.all()[0].content
        except IndexError:
            return ""

    # item_link is only needed if NewsItem has no get_absolute_url method.
    def item_link(self, item):
        return reverse('news-item', args=[item.pk])
