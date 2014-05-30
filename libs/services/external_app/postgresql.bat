rem the envrionment var will be set when running this script, so if this bat is run manually, the var will not be set, even 
rem the following codes are added
rem python configuration.py

rem set TOOLS_ROOT=%~dp0\tools
rem set POSTGRESQL_ROOT=%TOOLS_ROOT%\PostgreSQL\pgsql
chcp 65001
echo POSTGRESQL_ROOT is %POSTGRESQL_ROOT%
echo POSTGRESQL_PORT is %POSTGRESQL_PORT%

PATH=%POSTGRESQL_ROOT%\bin;%PATH%

title "PostgreSQL"

@ECHO ON
REM The script sets environment variables helpful for PostgreSQL
@SET PATH="%POSTGRESQL_ROOT%\bin";%PATH%
@SET PGDATA=%POSTGRESQL_ROOT%\..\..\data\data_post
@SET PGDATABASE=postgres
@SET PGUSER=postgres
@SET PGPORT=%POSTGRESQL_PORT%
@SET PGLOCALEDIR=%POSTGRESQL_ROOT%\share\locale
REM Next line MUST be uncommented the first time to init the server, it can then be commented.
if not exist %PGDATA% "%POSTGRESQL_ROOT%\bin\initdb" -U postgres -A trust -E UTF8
"%POSTGRESQL_ROOT%\bin\pg_ctl" -D "%POSTGRESQL_ROOT%/../../data/data_post" -l %POSTGRESQL_ROOT%/../../logfile start