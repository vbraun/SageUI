#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Add our custom widgets to glade3
"""

##############################################################################
#  SageUI: A graphical user interface to Sage, Trac, and Git.
#  Copyright (C) 2013  Volker Braun <vbraun.name@gmail.com>
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.
##############################################################################


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



