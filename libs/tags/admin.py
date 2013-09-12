from objsys.tree import register_menu

register_menu(u'tags/pane', u'tags', u'/')
#The following is a dynamic child. Children for tree will be get from /tags/
register_menu(u'tags/tagged', u'dynamic://tags', u'/tags')

