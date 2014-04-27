import logging
from django.core.context_processors import csrf
from objsys.add_tag_template_view import AddTagTemplateView
from ufs_utils.django_utils import retrieve_param
from ufs_utils.string_tools import unquote_unicode


class AddTagTemplateViewLocal(AddTagTemplateView):
    def __init__(self, **kwargs):
        super(AddTagTemplateViewLocal, self).__init__(**kwargs)

    def tag_url_list(self, url_list):
        for submitted_url in url_list:
            self.tag_url(submitted_url)

    def append_to_listed_urls(self, url):
        url = unquote_unicode(url)
        if not (url in self.listed_urls):
            self.listed_urls.append(url)

    def extend_listed_urls(self, urls):
        for url in urls:
            self.append_to_listed_urls(url)

    def get_context_data(self, **kwargs):
        #context = super(AddTagTemplateView, self).get_context_data(**kwargs)
        context = {}
        data = retrieve_param(self.request)

        #Load saved submitted_url
        if "saved_urls" in self.request.session:
            self.listed_urls = self.request.session["saved_urls"]

        close_flag = False

        if "tags" in data:
            self.tags = data["tags"]

        if "selected_url" in data:
            close_flag = True
            selected_url_params = data.getlist("selected_url")
            if type(selected_url_params) != list:
                selected_url_params = [selected_url_params]

            self.tag_url_list(selected_url_params)

        if "url" in data:
            url_param = data.getlist("url")
            if type(url_param) != list:
                url_param = [url_param]
            self.extend_listed_urls(url_param)

        for tagged_url in self.tagged_urls:
            if tagged_url in self.listed_urls:
                self.listed_urls.remove(tagged_url)

        self.request.session["saved_urls"] = self.listed_urls
        log = logging.getLogger(__name__)
        log.error(self.listed_urls)
        urls_with_tags = self.get_urls_with_tags()
        log.error(urls_with_tags)
        c = {"user": self.request.user, "close_flag": close_flag, "urls_with_tags": urls_with_tags,
             "new_url_input": False}
        if 0 == len(urls_with_tags):
            c["new_url_input"] = True
        c.update(csrf(self.request))
        context.update(c)
        #log = logging.getLogger(__name__)
        #log.error(context)
        return context