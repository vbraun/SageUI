#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Add our custom terminal widget to glade3
"""

import os
import sys


print 'terminal_plugin imported'

gui_path = os.path.split(os.path.split(__file__)[0])[0]
sys.path.append(gui_path)
sageui_path = os.path.split(os.path.split(gui_path)[0])[0]
sys.path.append(sageui_path)

for p in sys.path:
    print p

from terminal_widget import TerminalWidget
from diff_viewer_widget import DiffViewerWidget



