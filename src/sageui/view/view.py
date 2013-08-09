"""
The View
"""

import os
import sys
import gtk

from sageui.misc.cached_property import cached_property



class View(object):

    def __init__(self, presenter):
        self.presenter = presenter
        
    @cached_property
    def resource_dir(self):
        return os.path.dirname(sys.modules['sageui'].__file__)

    @cached_property
    def glade_file(self):
        return os.path.join(self.resource_dir, 'res', 'SageUI.xml')
        
    @cached_property
    def main_window(self):
        from main_window import MainWindow
        return MainWindow(self.glade_file)



