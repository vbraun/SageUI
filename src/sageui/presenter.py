"""
The Presenter (Controller)

Here is where it all comes together, the presenter ties together the
data model with the gui to create an application. It neither knows
about data nor about the gui, it just ties the two together.


"""



class Presenter(object):

    def __init__(self, view_class, model_class):
        self.view = view_class(self)
        self.model = model_class(self)
        self.view.main_window.show()

    
