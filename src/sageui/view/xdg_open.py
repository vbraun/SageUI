"""
Open with External Application

Uses xdg-open if possible, and platform-specific workarounds on other systems.
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
import subprocess
import logging




def xdg_open(file_or_uri, parent_window):
    """
    Open file or uri with external program.
    
    Uses xdg-open if possible, workarounds for other platforms.
    """
    presenter = parent_window
    if sys.platform.startswith('darwin'):
        _open_darwin(file_or_uri, presenter, parent_window)
    elif os.name == 'posix':
        _open_unix(file_or_uri, presenter, parent_window)
    elif os.name == 'nt':
        _open_windows(file_or_uri, presenter, parent_window)
    else:
        presenter.show_error(parent_window, 
                             'Unknown platform', 'Cannot display '+file_or_uri)


def _open_unix(file_or_uri, presenter, parent):
    try:
        rc = subprocess.call(['xdg-open', file_or_uri])
    except (IOError, OSError, RuntimeError) as err:
        presenter.show_error(str(type(err)), str(err))
        return
    logging.info('xdg_open returned %s', rc)
    if rc == 0:
        return
    elif rc == 1:
        presenter.show_error(parent, 'xdg-open failed', 'Error in command line syntax.')
    elif rc == 2:
        presenter.show_error(parent, 'xdg-open failed', 
                             'One of the files passed on the command line did not exist.')
    elif rc == 3:
        presenter.show_error(parent, 'xdg-open failed', 'A required tool could not be found.')
    elif rc == 4:
        presenter.show_error(parent, 'xdg-open failed', 'The action failed.')
    else:
        presenter.show_error(parent, 'xdg-open failed', 'Undefined error (rc={0}).'.format(rc))
    

def _open_windows(file_or_uri):
    try:
        subprocess.call(['open', file_or_uri])
    except (IOError, wOSError, RuntimeError) as err:
        presenter.show_error(parent, str(type(err)), str(err))
        return

def _open_windows(file_or_uri):
    try:
        os.startfile(filepath)
    except (IOError, OSError, RuntimeError) as err:
        presenter.show_error(parent, str(type(err)), str(err))
        return
