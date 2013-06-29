mkdir ..\data\beanstalkdData
if "%ufs_beanstalkd_port%"=="" (set ufs_beanstalkd_port=11300)
..\others\beanstalk\bin\beanstalkd.exe -b ../data/beanstalkdData -p %ufs_beanstalkd_port% -l 127.0.0.1