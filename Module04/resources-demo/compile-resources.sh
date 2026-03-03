#!/bin/bash

source .venv/bin/activate
pyside6-rcc --output src/resources_demo/resources_rc.py resources/resources.qrc
