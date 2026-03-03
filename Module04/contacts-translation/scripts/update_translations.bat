@echo off
for %%L in (de_DE en_GB es_ES) do (
    uv run pyside6-lupdate -target-language %%L -extensions .py src -ts resources/translations/translation_%%L.ts
)
