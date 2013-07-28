call activate.bat
ext_svr
if exist syncdb_needed.txt manage syncdb --noinput
rem python libs\services\apps\tube_logging_service.py --input "ufs_test_tube"
service_starter
tornado.bat