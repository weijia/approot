call activate.bat
rem xpython
if "%ufs_web_server_port%"=="" (set ufs_web_server_port=8012)
echo ufs_web_server_port is %ufs_web_server_port%
python tornado_main.py %ufs_web_server_port%