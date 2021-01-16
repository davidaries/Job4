from datetime import datetime
from tkinter import *
import language_dictionary as ld
# import datetime
# import time
# import home_screen
# import PEv1_data as pe_data
import query
from widgets import widgets as wd


class manage_window:
    """
    :param self.root: a reference to the root window for the UI
    :type self.root: Tkinter window
    :param self.log_window: a reference to the log window used for displaying data received from task window
    :type self.log_window: Tkinter window
    :param self.window: the window of this specific staffer
    :type: self.window: Tkinter window
    :param self.staff_name: the name of the staff member who owns the window
    :type self.staff_name: str
    :param self.staff_id: and identification of the staffers role
    :type self.staff_id: str
    :param self.language: the language preferences of the staff member
    :type self.language: str
    :param self.device_id: the unique identification of the staff member's screen
    :type self.device_id: int
    :param self.column_padding: a column padding length for spacing widgets in the staffers screen
    :type self.column_padding: int
    :param self.row_padding: a row padding length for spacing widgets in the staffers screen
    :type self.row_padding: int
    :param self.row_current: value used for managing placement to the grid layout of the home screen
    :type self.row_current: int
    :param self.task_row: value used for managing the placement of widgets in the task window
    :type self.task_row: int
    :param self.value_holder: a list created to store the values of widget items once they have been processed
    :type self.value_holder: list
    :param self.widgets: a list created to store the appropriate values for the widgets added to the task screen
    :type self.widgets: list
    :param self.token: the token value for the current job being processed by the staffer
    :type self.token: int
    :param self.token_list: storage of the current list of tokens TO BE USED FOR TIMED POLL OF PEO_Q
    :type self.token_list: list
    :param self.at_home: a value to store whether the user is currently in the home screen or not FOR POLLING EVERY 10 seconds
    :type self.at_home: bool
    """

    def __init__(self, window, staffer, log, device_id, root, home, sim_time):
        self.root = root
        self.home = home
        self.log_window = log
        self.window = window
        self.sim_time = sim_time
        self.staff_name = staffer.get('~1')
        self.staff_id = staffer.get('~23')
        self.language = staffer.get('~100')
        self.device_id = device_id
        self.column_padding = 80
        self.row_padding = 12
        self.row_current = 2
        self.task_row = 0
        self.value_holder = []
        self.widgets = []
        self.token = None
        self.token_list = []
        self.token_start_time = {}
        self.token_time_label = {}
        self.tokens_completed = []
        self.at_home = True
        self.widget_creator = wd(root, self.language, self.window)

    def get_device_id(self):
        return self.device_id

    def poll_controller(self):
        tasks = self.home.get_tasks(self.device_id)
        if tasks:
            for task in tasks:
                if task not in self.token_list and task not in self.tokens_completed:
                    self.token_start_time[task] = tasks.get(task)[6]
                    if self.at_home:
                        self.send_data(task, tasks.get(task))
                if task not in self.token_list and task not in self.tokens_completed:
                    self.token_list.append(task)
                if task in self.token_time_label and self.at_home and task not in self.tokens_completed:
                    self.update_wait_time(task)
        self.root.after(1000, self.poll_controller)

    def update_wait_time(self, token):
        display_t_diff = self.sim_time.get_time_difference(self.token_start_time.get(token))
        self.token_time_label.get(token).config(text=display_t_diff)

    def refresh_home(self):
        tasks = self.home.get_tasks(self.device_id)
        if tasks:
            self.clear_window()
            self.set_home()
            self.token_time_label.clear()
            for token in self.token_list:
                self.send_data(token, tasks.get(token))

    def send_data(self, token, raw_data):
        if self.at_home:
            task_id = raw_data[3]
            person_id = raw_data[0]
            task_window_info = raw_data[5]
            priority = raw_data[2]
            self.populate_task_btn(task_id, person_id, task_window_info, token, priority)
            self.row_current += 1

    def populate_task_btn(self, task_id, person_id, task_window_info, token, priority):
        """This function adds the buttons for the staffer's task to the task window.
        :param task_id: the value that corresponds to the task that the staffer needs to complete
        :type task_id: str
        :param person_id: the unique identification number of the person being processed by the staff member
        :type person_id: int
        :param task_window_info: contains a list of widget elements to be added to the task window for the staff member
        :type task_window_info: list
        :param token: the unique token id for the information handled by the staff member
        :type token: int"""
        task_name = ld.get_text_from_dict(self.language, task_id)
        self.add_person_to_tasks(person_id, priority, token)
        btn_action: Button = Button(self.window, text=task_name,
                                    command=lambda: self.write_task_screen(task_window_info, person_id, token, task_id),
                                    fg="black", bg="gray", height=1, width=10)
        btn_action.grid(column=3, row=self.row_current, ipadx=self.row_padding)
        self.row_current += 1

    def set_home(self):
        """This function sets up the home screen for the staffer"""
        self.window.title(ld.get_text_from_dict(self.language, self.staff_id))
        staff_name = Label(self.window, text=self.staff_name, font=self.widget_creator.larger_font)
        staff_name.grid(column=0, row=0)
        self.add_column_headers()

    def add_column_headers(self):
        """This function adds the headers for the tasks in the home screen (name     task)"""
        label_name = Label(self.window, text=ld.get_text_from_dict(self.language, '~1') + '\t',
                           font=self.widget_creator.medium_font)
        label_name.grid(column=0, row=self.row_current, ipady=self.row_padding, sticky='W')
        label_time = Label(self.window, text='  Time\t', font=self.widget_creator.medium_font)
        label_time.grid(column=1, row=self.row_current, ipady=self.row_padding)
        label_priority = Label(self.window, text='  Priority\t', font=self.widget_creator.medium_font)
        label_priority.grid(column=2, row=self.row_current, ipady=self.row_padding)
        label_event = Label(self.window, text=ld.get_text_from_dict(self.language, '~1'),
                            font=self.widget_creator.medium_font)
        label_event.grid(column=3, row=self.row_current, ipadx=self.column_padding, ipady=self.row_padding)
        self.row_current += 1

    def add_person_to_tasks(self, person_id, priority, token):
        """This function adds the name of a person who needs to be processed by the staffer
        :param person_id: identification number of the person
        :type person_id: int
        """
        name = query.adat_person_key(person_id, '~1')[1]  # maybe list handling should be done in query.py
        label_name = Label(self.window, text=name, font=self.widget_creator.medium_font)
        label_name.grid(column=0, row=self.row_current, ipady=self.row_padding, sticky='W')
        time_difference = self.sim_time.get_time_difference(self.token_start_time.get(token))
        label_time = Label(self.window, text=time_difference, font=self.widget_creator.medium_font)  # will be actual time
        self.token_time_label[token] = label_time
        label_time.grid(column=1, row=self.row_current, ipady=self.row_padding)
        label_priority = Label(self.window, text=priority, font=self.widget_creator.medium_font)
        label_priority.grid(column=2, row=self.row_current, ipady=self.row_padding)

    def write_task_screen(self, task_window_info, person_id, token, task_id):
        """This method writes the widgets to the task screen of the corresponding staffer
        :param token: unique token id for the given task
        :type token: int
        :param person_id: the unique identity number of the person being processed
        :type person_id: int
        :param task_window_info: list of task widgets that need to be added to the task screen
        :type task_window_info: list
        :param task_id: ~vocab reference to the task that needs to be completed by the staffer
        :type task_id: str
        """
        self.at_home = False
        self.clear_window()
        self.token = token
        for item in task_window_info:
            if item[0] == 'Fixed':
                self.widget_creator.add_label(item[1], person_id)
            elif item == 'PersonHeader':
                self.widget_creator.add_person_header(person_id)
            elif item == 'TaskHeader':
                self.widget_creator.add_task_header(task_id)
            elif item[0] == 'ModifyEntry':
                self.widget_creator.add_entry_with_text(item[1], person_id)
            elif item[0] == 'EmptyEntry':
                self.widget_creator.add_entry(item[1])
            elif item[0] == 'DropDown':
                self.widget_creator.add_drop_down(item[1:])
            elif item[0] == 'CheckBoxes':
                self.widget_creator.add_check_boxes(item[1:])
            elif item[0] == 'Button':
                self.add_button_submit(item[1], token)

    def clear_window(self):
        """This function clears the window that it is given allowing it to be a blank canvas before the window
        is populated with new data
        """
        for widget in self.window.winfo_children():
            widget.destroy()

    def add_button_submit(self, value, token):
        """this method adds a submit button to a given window
        :param value: a dictionary reference to a value that needs to be written in the form a label to the screen
        :type value: str
        """
        btn_submit = Button(self.window, text=ld.get_text_from_dict(self.language, value),
                            command=lambda: self.submit_btn_listener(token),
                            fg="black", bg="gray", height=1, width=10)
        btn_submit.grid(row=self.widget_creator.task_row, column=0, sticky='S')
        btn_return = Button(self.window, text=ld.get_text_from_dict(self.language, '~8'),  # ~8 for return/regresa
                            command=self.return_btn_listener,
                            fg="black", bg="gray", height=1, width=10)
        btn_return.grid(row=self.widget_creator.task_row, column=1, sticky='S')
        self.task_row += 1

    def return_btn_listener(self):
        self.token = None
        self.at_home = True
        self.value_holder.clear()
        self.widget_creator.clear_widget_data()
        self.refresh_home()

    def submit_btn_listener(self, token):
        """an action listener for the submit button.  As it stands, it only takes the staffer back to their home screen
        but this is where the addition of data to pdata and the log will go
        """
        self.manage_widgets()
        self.widgets.clear()
        self.clear_window()
        data_return = self.add_to_log()
        self.token = None
        self.at_home = True
        self.home.return_data(token, data_return)
        self.token_list.remove(token)
        self.token_start_time.pop(token)
        self.token_time_label.pop(token)
        self.tokens_completed.append(token)
        self.widget_creator.clear_widget_data()
        self.task_row = 10
        self.set_home()
        self.refresh_home()

    def add_to_log(self):
        """This function adds the data that will be sent back to the protocol manager to the log window
        print statement is so you can see how the actual value looks in the program not just the log printed version"""
        if len(self.value_holder) > 0:
            return_data = []
            for _ in range(len(self.value_holder)):
                return_data.append(self.value_holder.pop())
            return return_data
        else:
            return 'NO DATA GIVEN'

    def add_value(self, key, value):
        """This function adds a key value pair to the stored information retrieved from the widgets in the task screen
        :param key: the key corresponding to a dictionary reference in language_dictionary
        :type key: str
        :param value: the value retrieved from the widget in the task screen
        :type value: int or str"""
        try:
            if int(value):
                self.value_holder.append({'k': key, 'v': value, 'vt': 'float', 'units': '~41'})
            elif bool(value):
                self.value_holder.append({'k': key, 'v': value, 'vt': 'bool', 'units': None})
        except:
            if value[0] == '~':
                self.value_holder.append({'k': key, 'v': value, 'vt': 'vocab', 'units': None})
            else:
                self.value_holder.append({'k': key, 'v': value, 'vt': 'str', 'units': None})

    def manage_widgets(self):
        """This function loops through the widgets stored in the task screen for the staffer.  It's job is to retrieve
        the data from the widgets so they can be passed back to the protocol manage and currently prints to the log
        window.  Added exceptions for when there are no values given so empty lists are not added or displayed"""
        widgets = self.widget_creator.return_widget_data()
        for widget in widgets:
            if len(widget) == 3:
                if len(widget[1].get()) > 0:
                    self.add_value(widget[0], widget[2].get(widget[1].get()))

            elif widget[0][0] == '~18':  # if it is a checkbox input
                if widget[1][0].get() == 1:
                    self.add_value(widget[0][0], widget[1][1])
            else:
                if len(widget[1].get()) > 0:
                    self.add_value(widget[0], widget[1].get())
