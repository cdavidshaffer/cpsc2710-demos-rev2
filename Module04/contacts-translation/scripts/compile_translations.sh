#!/bin/bash


for file in resources/translations/translation*.ts; do
    uv run pyside6-lrelease ${file}
done

uv run pyside6-rcc --output src/contacts/resources_rc.py resources/resources.qrc
