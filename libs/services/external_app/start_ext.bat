call syncdb.bat
python libs\services\apps\tube_logging_service.py --input "ufs_test_tube"
rem python libs\services\service_starter.py
echo calling runserver.bat
call runserver.bat
