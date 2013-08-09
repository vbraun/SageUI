"""
The Application

The application class is basically just a container to hold
Model/View/Presenter. There is only one instance. On the debug REPL
(if you start with the ``--debug`` option) it is assigned to the
variable ``app`` in the global namespace.
"""

from sageui.presenter import Presenter
from sageui.view.view import View
from sageui.model.model import Model


class Application(object):

    def __init__(self):
        self.presenter = Presenter(View, Model)
        self.view = self.presenter.view
        self.model = self.presenter.model
        



