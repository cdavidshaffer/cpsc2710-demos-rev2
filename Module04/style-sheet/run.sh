#!/bin/bash

uv run pyside6-rcc --output src/style_sheet/resources_rc.py resources/resources.qrc 
uv run demo
