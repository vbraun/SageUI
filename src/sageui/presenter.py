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
        self.show_trac()

    def terminate(self):
        """
        Quit the program
        """
        self.view.terminate()
        self.model.terminate()

    def show_about(self):
        self.view.about_dialog.show()

    def hide_about(self):
        self.view.about_dialog.hide()

    def show_trac(self):
        ticket_list = self.model.trac.database.recent_tickets()
        self.view.trac_window.set_ticket_list(ticket_list)
        self.view.trac_window.show()

    def trac_ticket_selected(self, ticket):
        self.view.trac_window.display_ticket(ticket)

    def hide_trac(self):
        self.view.trac_window.hide()

    def show_notification(self, text):
        self.view.new_notification_dialog(text).show()

    def hide_notification(self):
        self.view.hide_notification_dialogs()
