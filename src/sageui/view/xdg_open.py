"""
Open with external application
"""

import os
import sys
import subprocess





def xdg_open(file_or_uri, presenter):
    """
    Open file or uri with external program.
    
    Uses xdg-open if possible, workarounds for other platforms.
    """
    if sys.platform.startswith('darwin'):
        _open_darwin(file_or_uri, presenter)
    elif os.name == 'posix':
        _open_unix(file_or_uri, presenter)
    elif os.name == 'nt':
        _open_windows(file_or_uri, presenter)
    else:
        presenter.show_error('Unknown platform', 'Cannot display '+file_or_uri)


def _open_unix(file_or_uri, presenter):
    try:
        rc = subprocess.call(['xdg-open', file_or_uri])
    except (IOError, OSError, RuntimeError) as err:
        presenter.show_error(str(type(err)), str(err))
        return
    print 'xdg_open returned', rc
    if rc == 0:
        return
    elif rc == 1:
        presenter.show_error('xdg-open failed', 'Error in command line syntax.')
    elif rc == 2:
        presenter.show_error('xdg-open failed', 
                             'One of the files passed on the command line did not exist.')
    elif rc == 3:
        presenter.show_error('xdg-open failed', 'A required tool could not be found.')
    elif rc == 4:
        presenter.show_error('xdg-open failed', 'The action failed.')
    else:
        presenter.show_error('xdg-open failed', 'Undefined error (rc={0}).'.format(rc))
    

def _open_windows(file_or_uri):
    try:
        subprocess.call(['open', file_or_uri])
    except (IOError, wOSError, RuntimeError) as err:
        presenter.show_error(str(type(err)), str(err))
        return

def _open_windows(file_or_uri):
    try:
        os.startfile(filepath)
    except (IOError, OSError, RuntimeError) as err:
        presenter.show_error(str(type(err)), str(err))
        return
