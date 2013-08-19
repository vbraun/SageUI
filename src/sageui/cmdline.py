"""
Handle Command Line Options and Launch the Sage UI
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


import sys
import os
import importlib
import logging




def check_gui_prerequisites():
    try:
        from gi.repository import Gtk
    except ImportError:
        logging.critical('You need the Python GTK interface!')
        sys.exit(1)
    try:
        import cairo
    except ImportError:
        logging.critical('You need the Python Cairo interface!')
        sys.exit(1)
    try: 
        from gi.repository import Vte
    except ImportError:
        logging.critical('You need VTE!')
        sys.exit(1)


def debug_shell(app):
    from IPython.lib.inputhook import enable_gtk3
    enable_gtk3()
    from IPython.frontend.terminal.ipapp import TerminalIPythonApp
    ip = TerminalIPythonApp.instance()
    ip.initialize(argv=[])
    ip.shell.enable_gui('gtk3')
    ip.shell.user_global_ns['app'] = app
    ip.shell.user_global_ns['repo'] = app.model.repo
    ip.shell.user_global_ns['git'] = app.model.repo.git
    def ipy_import(module_name, identifier):
        module = importlib.import_module(module_name)
        ip.shell.user_global_ns[identifier] = getattr(module, identifier) 
    ipy_import('sageui.model.git_interface', 'GitInterface')
    ipy_import('sageui.model.git_repository', 'GitRepository')
    ip.start()




def launch_gui(debug=False):
    check_gui_prerequisites()
    from sageui.app import Application
    app = Application()
    if debug:
        debug_shell(app)
    else:
        from gi.repository import Gtk
        # workaround for https://bugzilla.gnome.org/show_bug.cgi?id=622084
        import signal
        signal.signal(signal.SIGINT, signal.SIG_DFL)
        # end workaround
        Gtk.main()



description = """
    The Sage UI ..."""


def run_doctests(args):
    from sage.doctest.control import DocTestController
    DC = DocTestController(*args)
    err = DC.run()
    sys.exit(err)


def launch():
    from argparse import ArgumentParser
    parser = ArgumentParser(description=description)
    parser.add_argument('--debug', dest='debug', action='store_true',
                        default=False, 
                        help='debug')
    parser.add_argument('--doctest', dest='doctest', action='store_true',
                        default=False, 
                        help='doctest')
    parser.add_argument('--log', dest='log', default=None,
                        help='one of [DEBUG, INFO, ERROR, WARNING, CRITICAL]')
    args = parser.parse_args()
    if args.log is not None:
        level = getattr(logging, args.log)
        logging.basicConfig(level=level)
    if args.doctest:
        run_doctests(args)
    else:
        launch_gui(debug=args.debug)
