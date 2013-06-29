rem set TOOLS_ROOT=%~dp0\tools
rem set SOFTWARE_ROOT=%TOOLS_ROOT%\PostgreSQL\pgsql\bin
set SOFTWARE_ROOT="..\others\pgsql\bin"

title "pgAdmin III"

start %SOFTWARE_ROOT%\pgAdmin3.exe
exit