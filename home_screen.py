from tkinter import *
from manage_window import manage_window
import datetime
import PEv1_data as PEd
from login_manager import login_manager as lm


class home_screen:
    """The home_screen class is in charge of creating and managing the home screens for the various staffers
    based on the different kinds of staff windows, the handling of the person populated on their task list
    will be done based on their job type
    :param self.main_program: reference to the main tk program used for the creation of additional windows
    :type self.main_program: tk class
    :param self.horizontal_spacing: value used to space the windows horizontally across the screen
    :type self.horizontal_spacing: int
    :param self.log_window_pointer: pointer to reference the log window which is needed to write data to the log window
    :type self.log_window_pointer: tk class
    :param self.column_padding: value used to space out values placed into a window
    :type self.column_padding: int
    :param self.row_padding: value used to pad rows to make the spacing between them larger
    :type self.row_padding: int
    :param self.row_current: value used to place values in the home screen in the appropriate rows
    :type self.row_current: int
    :param self.task_row: value used to increment the current row placement
    :type self.task_row: int
    :param self.reception_home: the window that holds a reference to the receptionist's window
    :type self.reception_home: tk Window
    :param self.assistant_home: the window that holds a reference to the assistant's window
    :type self.assistant_home: tk Window
    :param self.provider_home: the window that holds a reference to the provider's window
    :type self.provider_home: tk Window
    :param self.lab_tech_home: the window that holds a reference to the lab tech's window
    :type self.reception_home: tk Window"""

    def __init__(self, master, log_window, controller, sim_time):
        self.opening_time = 1609340400
        self.controller = controller
        self.sim_time = sim_time
        self.root = master
        self.horizontal_spacing = 0
        self.log_window_pointer = log_window
        self.column_padding = 80
        self.row_padding = 12
        self.row_current = 2
        self.task_row = 0
        self.staff_windows = []
        self.staff_dict = {}
        self.staff_dict_new = {}
        self.staff_login = []
        self.loop_count = 0
        self.login_widgets = None
        self.home = None
        self.win_num = 0

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
        self.win_num+=1
        window = self.create_home_screen('+150')
        login_manager = lm(self.root, '~101', self.home, window)
        login_manager.add_entry_id()
        login_manager.add_entry_password()
        login_manager.login_button()

    def login_success(self, staffer_id, window):
        """"""
        device_id = PEd.staff_device.get(staffer_id)
        staff_info = PEd.staffers.get(staffer_id)
        self.staff_dict[device_id] = manage_window(window, staff_info, self.log_window_pointer,
                                                   device_id, self.root, self.home, self.sim_time)

        self.staff_dict[device_id].clear_window()
        self.staff_dict[device_id].set_home()
        self.staff_dict[device_id].poll_controller()

    def add_home(self, home):
        self.home = home

    def get_tasks(self, device_id):
        return self.controller.poll_tasks(device_id)

    def return_data(self, token, data_return):
        sample_data = data_return
        self.controller.return_completion(token, sample_data)
