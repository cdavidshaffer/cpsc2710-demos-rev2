---
name: pyside-test-widget
description: >
  Use when the user wants a pytest-qt
  test skeleton for a PySide6 widget.
argument-hint: "[widget_file] [ClassName]"
arguments: [widget_file, class_name]
context: fork
disable-model-invocation: true
---

1. Run scripts/make_test_skeleton.py $widget_file $class_name.
2. Fill in real assertions -- the skeleton only stubs one test per public method, using the qtbot fixture from pytest-qt.

If $ARGUMENTS is empty, stop and report that widget_file and class_name are both required.
