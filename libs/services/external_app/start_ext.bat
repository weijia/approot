rem call activate.bat
python -u libs\services\external_app\ext_svr.py
if exist syncdb_needed.txt call syncdb.bat
rem python libs\services\apps\tube_logging_service.py --input "ufs_test_tube"
python libs\services\svc_base\service_starter.py
echo calling runserver.bat
rem call runserver.bat
rem call tornado.bat
rem python -u cherrypy_server.py
