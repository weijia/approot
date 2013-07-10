from ui_framework.objsys.tree import register_menu

register_menu(u'filemanager/root', u'folders', u'/')
#The following is a dynamic child. Children for tree will be get from /tags/
register_menu(u'filemanager/root', u'dynamic://filemanager/root', u'/folders')