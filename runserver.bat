call ..\..\..\venv\Scripts\activate.bat
rem xpython
rem the envrionment var will be set when running this script, so if this bat is run manually, the var will not be set, even 
rem the following codes are added
rem python configuration.py
if "%ufs_web_server_port%"=="" (set ufs_web_server_port=8012)
echo ufs_web_server_port is %ufs_web_server_port%
python -u manage.py runserver %ufs_web_server_port%