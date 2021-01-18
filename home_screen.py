from tkinter import *
from manage_window import manage_window
import PEv1_data as PEd
from login_manager import login_manager as lm


class home_screen:
    """The home_screen class is in charge of creating and managing the home screens for the various staffers
    based on the different kinds of staff windows, the handling of the person populated on their task list
    will be done based on their job type in manage_window module
    :param self.controller: a reference to the controller module
    :type self.controller: module
    :param self.sim_time: a reference to the system_time module used to manage the timing of the simulation
    :type self.sim_time: module
    :param self.root: reference to the main tk program used for the creation of additional windows
    :type self.root: tk class reference
    :param self.log_window_pointer: pointer to reference the log window which is needed to write data to the log window
    :type self.log_window_pointer: tk module
    :param self.horizontal_spacing: value used to space the windows horizontally across the screen
    :type self.horizontal_spacing: int
    :param self.column_padding: value used to space out values placed into a window
    :type self.column_padding: int
    :param self.row_padding: value used to pad rows to make the spacing between them larger
    :type self.row_padding: int
    :param self.row_current: value used to place values in the home screen in the appropriate rows
    :type self.row_current: int
    :param self.task_row: value used to increment the current row placement
    :type self.task_row: int
    :param self.staff_dict: stores the tk window of a staffer where the dict key is their staff_id
    :type self.staff_dict: dict
    :param self.staff_login: is
    :param self.home: a reference to the home_screen module created in main.py given to children windows so data
    can be returned in teh future
    :type self.home: module reference"""

    def __init__(self, master, log_window, controller, sim_time):
        """Sets up the home_screen module
        :param master: a reference to the master window for the UI
        :type master: tk window reference
        :param log_window: no longer in use but kept around incase it might be useful in the future.  This is a
        reference to the log window information can be displayed
        :type log_window: tk window
        :param controller: a reference to the controller class used to send data back and forth from the UI
        :type controller: module
        :param sim_time: a reference to the system_time module used for recording current time in the simulation
        :type sim_time: module
        """
        self.controller = controller
        self.sim_time = sim_time
        self.root = master
        self.log_window_pointer = log_window
        self.horizontal_spacing = 0
        self.column_padding = 80
        self.row_padding = 12
        self.row_current = 2
        self.task_row = 0
        self.staff_dict = {}
        self.home = None

    def create_home_screen(self, v):
        """In charge of the creation of a new window to be displayed on the screen
        :param v: is a value used for the vertical spacing of the staffers windows in the UI
        :type v: str
        :return: a reference to a window so it can be edited in the future
        :rtype: Window"""
        home = Toplevel(self.root)
        home.geometry("400x300+" + self.horizontal_spacing.__str__() + v)
        self.horizontal_spacing += 450
        return home

    def login_screen(self):
        """This function creates the login screen for the various staffer by making calls to the login_manager
        module"""
        window = self.create_home_screen('+150')
        login_manager = lm(self.root, '~101', self.home, window)
        login_manager.add_entry_id()
        login_manager.add_entry_password()
        login_manager.login_button()

    def login_all(self):
        """This function creates a window for all available staff members and bypasses the login screen for all of
        those staff members"""
        for staff in PEd.staffers:
            window = self.create_home_screen('+150')
            staff_info = PEd.staffers.get(staff)
            device_id = PEd.staff_device.get(staff)
            PEd.staffer_login_info.get(staff).__setitem__(1, True)
            self.staff_dict[device_id] = manage_window(window, staff_info, self.log_window_pointer,
                                                       device_id, self.root, self.home, self.sim_time)

            self.staff_dict[device_id].clear_window()
            self.staff_dict[device_id].set_home()
            self.staff_dict[device_id].poll_controller()

    def login_success(self, staffer_id, window):
        """After a successful login from a staffer, this function creates a home screen for them with their
        corresponding tasks.
        :param staffer_id: the unique id of a staffer
        :type staffer_id: str
        :param window: a reference to the associated tkinter window
        :type window: tk window"""
        device_id = PEd.staff_device.get(staffer_id)
        staff_info = PEd.staffers.get(staffer_id)
        self.staff_dict[device_id] = manage_window(window, staff_info, self.log_window_pointer,
                                                   device_id, self.root, self.home, self.sim_time)

        self.staff_dict[device_id].clear_window()
        self.staff_dict[device_id].set_home()
        self.staff_dict[device_id].poll_controller()

    def add_home(self, home):
        """Sets a reference to home_screen that is later passed to the staffer windows so data can be sent back to
        home_screen module, which has a connection with the controller module
        :param home: reference to the home_screen module
        :type home: class reference
        """
        self.home = home

    def get_tasks(self, device_id):
        """This function returns the current list of tasks for a staffer based on their device_id
        :param device_id: a unique id for the staffers device
        :type device_id: str"""
        return self.controller.poll_tasks(device_id)

    def return_data(self, token, data_return):
        """This function sends the appropriate data for the token in question to be processed by the controller
        :param token: unique token id used for tasks
        :type token: int
        :param data_return: list of the corresponding data for the token
        :type data_return: list"""
        self.controller.return_completion(token, data_return)
