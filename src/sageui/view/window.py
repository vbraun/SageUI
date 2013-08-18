


class Window(object):

    def __init__(self, builder, window_object_id):
        self.window = builder.get_object(window_object_id)

    def show(self):
        """
        Show window. 

        If the window is already visible, nothing is done.
        """
        self.window.show()

    def present(self):
        """
        Bring to the user's attention
        
        Implies :meth:`show`. If the window is already visible, this 
        method will deiconify / bring it to the foreground as necessary.
        """
        self.window.present()

    def hide(self):
        self.window.hide()

    def destroy(self):
        return self.window.destroy()


