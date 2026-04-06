#!/bin/bash

for file in resources/translations/translation*.ts; do
    uv run pyside6-lrelease ${file}
done
