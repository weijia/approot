call ..\..\..\venv\Scripts\activate.bat
rem xpython
python manage.py schemamigration objsys --auto
python manage.py migrate