call activate.bat
ext_svr
manage syncdb --noinput
rem python libs\services\apps\tube_logging_service.py --input "ufs_test_tube"
rem python libs\services\service_starter.py
tornado.bat