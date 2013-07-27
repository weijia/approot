call activate.bat
ext_svr
manage syncdb --noinput
rem python libs\services\apps\tube_logging_service.py --input "ufs_test_tube"
service_starter
rem tornado.bat
cherrypy_server