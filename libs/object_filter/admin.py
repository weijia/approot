from objsys.tree import register_menu

try:
    register_menu(u'/object_filter', u'object_filter', u'/')
    register_menu(u'/object_filter/table/', u'diagram_table', u'/')
except:
    pass
