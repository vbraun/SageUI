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
        if self.model.config.sage_root is None:
            self.show_setup_assistant(None, self.setup_assistant_first_run_finished)
        else:
            self.show_git_window()
            #self.show_commandline_window()
            #self.show_trac_window()

    def terminate(self):
        """
        Quit the program
        """
        self.model.terminate()
        self.view.terminate()
        
    ###################################################################
    # The window containing the commandline terminal

    def show_commandline_window(self):
        return self.view.show_commandline_window(self.model.config.sage_root, 'sage')

    def hide_commandline_window(self):
        self.view.hide_commandline_window()
        if not self.view.have_open_window():
            self.terminate()

    ###################################################################
    # The git window

    def show_git_window(self):
        return self.view.show_git_window(self.model.config.sage_root)

    def hide_git_window(self):
        self.view.hide_git_window()
        if not self.view.have_open_window():
            self.terminate()

    def show_current_branch(self):
        local_branches = self.model.list_branches()
        current_branch = self.model.current_branch()
        self.view.set_git_branches(local_branches, current_branch)

    def checkout_branch(self, branch_name, ticket_number=None):
        branch = self.model.checkout_branch(branch_name, ticket_number)
        branches = self.model.list_branches()
        self.view.set_git_branches(branches, branch)

    ###################################################################
    # Preferences dialog

    def show_preferences_dialog(self):
        self.view.show_preferences_dialog(self.model.config)
        
    def apply_preferences_dialog(self):
        self.view.apply_preferences_dialog(self.model.config)

    def hide_preferences_dialog(self):
        self.view.hide_preferences_dialog()
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
        if not self.view.trac_window_constructed:
            current_ticket = self.model.trac.get_current_ticket()
            ticket_list = self.model.trac.get_ticket_list()
            self.view.trac_window.set_ticket_list(ticket_list, current_ticket)
            if current_ticket is not None:
                self.view.trac_window.display_ticket(current_ticket)
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
    
    def load_ticket(self, ticket_number, use_cache=False):
        if not (use_cache and self.model.trac.is_cached(ticket_number)):
            try:
                self.model.trac.load(ticket_number) 
            except TracError as msg:
                return self.show_error('Cannot download ticket', str(msg))
        self.model.trac.set_current_ticket(ticket_number)
        loaded_ticket = self.model.trac.get_current_ticket()
        ticket_list = self.model.trac.get_ticket_list()
        self.view.trac_window.set_ticket_list(ticket_list, loaded_ticket)
        self.view.trac_window.display_ticket(loaded_ticket)

    ###################################################################
    # Misc. notification dialog (modal)

    def show_notification(self, text):
        self.view.new_notification_dialog(text).show()

    def destroy_modal_dialog(self):
        self.view.destroy_modal_dialog()
        if not self.view.have_open_window():
            self.terminate()
 
    ###################################################################
    # Error dialog (modal)

    def show_error(self, title, text):
        self.view.new_error_dialog(title, text).show()

    ###################################################################
    # Setup assistant (modal)

    def sage_installation(self, sage_root):
        """
        Return data about the Sage installation at ``sage_root``
    
        INPUT:

        - ``sage_root`` -- a directory name or ``None`` (default). The 
          path will be searched if not specified.
        """
        return self.model.sage_installation(sage_root)

    def show_setup_assistant(self, sage_root, callback):
        """
        Assistant to figure out SAGE_ROOT
        
        INPUT:

        - ``sage_root`` -- string or ``None``. The initial value for 
          ``SAGE_ROOT``. If ``None``: Will be figured out from 
          calling ``sage`` in the ``$PATH``.
    
        - ``callback`` -- function / method. Will be called back with 
          the new :class:`sageui.model.sage_installation.SageInstallation`
        """
        self.view.new_setup_assistant(sage_root, callback).show()

    def setup_assistant_first_run_finished(self, sage_install):
        """
        The callback for the first run
        """
        self.model.config.sage_root = sage_install.sage_root
        self.model.config.sage_version = sage_install.version
        if not self.view.have_open_window():
            self.show_commandline_window()

    ###################################################################
    # open with external program

    def xdg_open(self, file_or_uri):
        self.view.xdg_open(file_or_uri)

    ###################################################################
    # Handle configuration change

    def config_sage_changed(self):
        self.model.sage_changed()
        self.view.config_sage_changed(self.model.config)
        
