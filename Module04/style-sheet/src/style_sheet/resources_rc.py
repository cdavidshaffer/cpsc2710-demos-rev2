# Resource object code (Python 3)
# Created by: object code
# Created by: The Resource Compiler for Qt version 6.10.2
# WARNING! All changes made in this file will be lost!

from PySide6 import QtCore

qt_resource_data = b"\
\x00\x00\x02\x01\
D\
emoWindow {\x0a    \
background-color\
: white;\x0a}\x0a\x0aQPus\
hButton, QCheckB\
ox {\x0a    backgro\
und-color: rgb(2\
40, 240, 240);\x0a \
   color: black;\
\x0a}\x0a\x0aQPushButton \
{\x0a    border-rad\
ius: 3px;\x0a    pa\
dding: 10px 10px\
;\x0a    margin: 3p\
x 5px 3px 5px;\x0a \
   border: 3px o\
utset grey;\x0a}\x0a\x0aQ\
CheckBox {\x0a    f\
ont-size: 18pt;\x0a\
}\x0a\x0aQPushButton:p\
ressed {\x0a    bor\
der: 3px inset g\
rey;\x0a}\x0a\x0aQPushBut\
ton#delete-butto\
n {\x0a    color: r\
ed;\x0a}\x0a\x0aQPushButt\
on[class=\x22specia\
l\x22] {\x0a    color:\
 green;\x0a}\x0a\x0a:hove\
r {\x0a    backgrou\
nd-color: blue;\x0a\
}\x0a\x0a:checked {\x0a  \
  color: pink;\x0a}\
\
"

qt_resource_name = b"\
\x00\x0b\
\x0ck<\xf3\
\x00s\
\x00t\x00y\x00l\x00e\x00s\x00h\x00e\x00e\x00t\x00s\
\x00\x09\
\x00(\xad#\
\x00s\
\x00t\x00y\x00l\x00e\x00.\x00q\x00s\x00s\
"

qt_resource_struct = b"\
\x00\x00\x00\x00\x00\x02\x00\x00\x00\x01\x00\x00\x00\x01\
\x00\x00\x00\x00\x00\x00\x00\x00\
\x00\x00\x00\x00\x00\x02\x00\x00\x00\x01\x00\x00\x00\x02\
\x00\x00\x00\x00\x00\x00\x00\x00\
\x00\x00\x00\x1c\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\
\x00\x00\x01\x9c\xbav\xec\x19\
"

def qInitResources():
    QtCore.qRegisterResourceData(0x03, qt_resource_struct, qt_resource_name, qt_resource_data)

def qCleanupResources():
    QtCore.qUnregisterResourceData(0x03, qt_resource_struct, qt_resource_name, qt_resource_data)

qInitResources()
