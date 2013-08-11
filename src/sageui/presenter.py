"""
The Presenter (Controller)

Here is where it all comes together, the presenter ties together the
data model with the gui to create an application. It neither knows
about data nor about the gui, it just ties the two together.


"""

from model.trac_error import TracError


class Presenter(object):

    def __init__(self, view_class, model_class):
        self.view = view_class(self)
        self.model = model_class(self)
        self.show_commandline_window()
        self.show_trac_window()

    def terminate(self):
        """
        Quit the program
        """
        self.model.terminate()
        self.view.terminate()
        
    ###################################################################
    # The window containing the commandline terminal

    def show_commandline_window(self):
        return self.view.show_commandline_window()

    def hide_commandline_window(self):
        self.view.hide_commandline_window()
        if not self.view.have_open_window():
            self.terminate()

    ###################################################################
    # The about dialog

    def show_about_dialog(self):
        self.view.about_dialog.show()

    def hide_about_dialog(self):
        self.view.about_dialog.hide()

    ###################################################################
    # The window containing the Sage trac tickets

    def show_trac_window(self):
        current_ticket = self.model.trac.get_current_ticket()
        ticket_list = self.model.trac.database.recent_tickets()
        self.view.trac_window.set_ticket_list(ticket_list, current_ticket)
        self.view.show_trac_window()
    
    def hide_trac_window(self):
        self.view.hide_trac_window()
        if not self.view.have_open_window():
            self.terminate()

    def ticket_selected(self, ticket_number):
        self.model.trac.set_current_ticket(ticket_number)
        ticket = self.model.trac.get_current_ticket()
        self.view.trac_window.set_current_ticket(ticket)
        self.view.trac_window.display_ticket(ticket)
    
    def load_ticket(self, ticket_number):
        try:
            self.model.trac.load(ticket_number) 
        except TracError as msg:
            return self.show_error('Cannot download ticket', str(msg))
        self.model.trac.set_current_ticket(ticket_number)
        loaded_ticket = self.model.trac.get_current_ticket()
        ticket_list = self.model.trac.database.recent_tickets()
        self.view.trac_window.set_ticket_list(ticket_list, loaded_ticket)
        self.view.trac_window.display_ticket(loaded_ticket)

    ###################################################################
    # Misc. notification dialog (modal)

    def show_notification(self, text):
        self.view.new_notification_dialog(text).show()

    def destroy_modal_dialog(self):
        self.view.destroy_modal_dialog()
 
    ###################################################################
    # Error dialog (modal)

    def show_error(self, title, text):
        self.view.new_error_dialog(title, text).show()

