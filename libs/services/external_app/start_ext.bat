rem call activate.bat
python -u libs\services\external_app\ext_svr.py
call syncdb.bat
rem python libs\services\apps\tube_logging_service.py --input "ufs_test_tube"
python libs\services\svc_base\service_starter.py
echo calling runserver.bat
call runserver.bat
