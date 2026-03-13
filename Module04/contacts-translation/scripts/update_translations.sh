#!/bin/bash

for lang in de_DE es_ES en_GB; do
    uv run pyside6-lupdate -target-language ${lang} -extensions .py src -ts resources/translations/translation_${lang}.ts
done
