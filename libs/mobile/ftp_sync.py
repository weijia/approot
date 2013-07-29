from kivy.uix.modalview import ModalView
from kivy.uix.listview import ListView
from kivy.uix.gridlayout import GridLayout
from kivy.lang import Builder
from kivy.adapters.models import SelectableDataItem
from kivy.properties import ObjectProperty

Builder.load_string("""
<ListViewModal>:
    list_view: list_view
    size_hint: None, None
    ListView:
        id: list_view
""")


class DataItem(SelectableDataItem):
    def __init__(self, text='', is_selected=False):
        self.text = text
        self.is_selected = is_selected


class ListViewModal(ModalView):
    list_view = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(ListViewModal, self).__init__(**kwargs)

        items = self.list_view.adapter.data
        item = u"ftp://a:b@c.com"
        items.append(item)


class MainView(GridLayout):
    def __init__(self, **kwargs):
        kwargs['cols'] = 1
        super(MainView, self).__init__(**kwargs)

        listview_modal = ListViewModal()

        self.add_widget(listview_modal)


if __name__ == '__main__':
    from kivy.base import runTouchApp
    runTouchApp(MainView(width=800))