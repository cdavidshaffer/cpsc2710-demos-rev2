@echo off
for %%L in (de_DE en_GB es_ES) do (
    uv run pyside6-lrelease resources\translations\translation_%%L.ts
)

uv run pyside6-rcc --output src\contacts\resources_rc.py resources\resources.qrc
