#noinspection PyBroadException
try:
    from collection_management.tree import register_menu

    register_menu(u'/object_filter', u'object_filter', u'/')
    register_menu(u'/object_filter/table/', u'diagram_table', u'/')
except ImportError:
    pass
except Exception:
    pass
