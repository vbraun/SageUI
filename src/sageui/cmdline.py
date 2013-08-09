"""
Handle Command Line Options and Launch the Sage UI
"""

import sys
import os


def check_gui_prerequisites():
    try:
        import gtk
    except ImportError:
        print 'Fatal: You need the Python GTK interface!'
        sys.exit(1)
    try:
        import pygtk
        pygtk.require('2.0')
    except ImportError:
        print 'Fatal: You need PyGTK version 2 or higher!'
        sys.exit(1)
    try:
        import gtk.glade
    except ImportError:
        print 'Fatal: You need the Python Glade interface!'
        sys.exit(1)
    try:
        import cairo
    except ImportError:
        print 'Fatal: You need the Python Cairo interface!'
        sys.exit(1)
    try: 
        import vte
    except ImportError:
        print 'Fatal: You need VTE!'
        sys.exit(1)


def launch_gui(debug=False):
    check_gui_prerequisites()
    from sageui.view.app import Application
    app = Application()
    if debug:
        from IPython.lib.inputhook import enable_gtk
        enable_gtk()
        from IPython.frontend.terminal.ipapp import TerminalIPythonApp
        ip = TerminalIPythonApp.instance()
        ip.initialize(argv=[])
        ip.shell.enable_gui('gtk')
        ip.shell.user_global_ns['app'] = app
        ip.start()
    else:
        import gtk
        gtk.main()



description = """
    The Sage UI ..."""



def launch():
    from argparse import ArgumentParser
    parser = ArgumentParser(description=description)
    parser.add_argument('--debug', dest='debug', action='store_true',
                        default=False, 
                        help='debug')
    args = parser.parse_args()
    print args
    launch_gui(debug=args.debug)
