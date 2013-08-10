


class Window(object):

    def __init__(self, builder, window_object_id):
        self.window = builder.get_object(window_object_id)

    def show(self):
        self.window.show()

    def hide(self):
        self.window.hide()

    def destroy(self):
        return self.window.destroy()


