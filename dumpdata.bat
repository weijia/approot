call ..\..\..\venv\Scripts\activate.bat
rem xpython
python manage.py dumpdata %1 > initial_data.json