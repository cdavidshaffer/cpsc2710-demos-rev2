@echo off
call .venv\Scripts\activate
pyside6-rcc --output src\resources_demo\resources_rc.py resources\resources.qrc
