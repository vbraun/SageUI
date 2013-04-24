"""
Handle Command Line Options and Launch the Sage UI
"""

import sys
import os


def check_gui_prerequisites():
    try:
        import pygtk
        pygtk.require('2.0')
    except:
        print 'You need PyGTK version 2 or higher!'
        sys.exit(1)
    try:
        import gtk
        import gtk.glade
    except:
        print 'You need the Python Glade interface!'
        sys.exit(1)
    try:
        import cairo
    except:
        print 'You need the Python Cairo interface!'
        sys.exit(1)
    try: 
        import vte
    except:
        print 'You need VTE!'
        sys.exit(1)


def launch_gui():
    check_gui_prerequisites()
    import gtk
    from sageui.gui.app import Application
    app = Application()
    gtk.main()


description = """
    The Sage UI ..."""



def launch():
    from argparse import ArgumentParser
    parser = ArgumentParser(description=description)
    parser.add_argument('--gui', dest='gui', action='store_true',
                        default=True, 
                        help='start the gui')
    args = parser.parse_args()
    
    if args.gui:
        launch_gui()
