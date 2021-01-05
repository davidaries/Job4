from tkinter import *
import language_dictionary as ld
import data
import datetime
import home_screen


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

    def __init__(self, window, staffer, log, device_id, root, home):
        self.root = root
        self.home = home
        self.log_window = log
        self.window = window
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
        self.at_home = True

    def get_device_id(self):
        return self.device_id

    # def poll_peo_q(self):
    #     """This function polls for data from peo_q and populates the staffer's home screen with the name of the
    #     person and the task they must complete.  This function calls itself every 10 seconds to see if there is
    #     new data in peo_q.
    #     """
    #     poll_data = data.get_data('peo_q', 0, self.device_id)
    #     for process in poll_data:
    #         person_id = process[2]
    #         task_id = process[12]
    #         task_window_info = process[14]
    #         token = process[1]
    #         # if self.at_home and not self.token_list.__contains__(token):   FOR USE WITH POLLING EVERY 10 SECONDS
    #         # self.token_list.append(token) FOR POLLING
    #         self.populate_task_btn(task_id, person_id, task_window_info, token)
    #         self.row_current += 1
    #     # self.root.after(10000,self.poll_peo_q)    FOR USE WITH POLLING EVERY 10 SECONDS
    def send_data(self, token, raw_data):
        # if [token,raw_data] not in self.token_list:
        #     self.token_list.append([token,raw_data])
        if self.at_home:
            self.clear_window()
            self.set_home()
            task_id = raw_data[3]
            person_id = raw_data[0]
            task_window_info = raw_data[5]
            self.populate_task_btn(task_id, person_id, task_window_info, token)
            self.row_current+=1

    def populate_task_btn(self, task_id, person_id, task_window_info, token):
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
        self.add_person_to_tasks(person_id)
        btn_action: Button = Button(self.window, text=task_name,
                                    command=lambda: self.write_task_screen(task_window_info, person_id, token, task_id),
                                    fg="black", bg="gray", height=1, width=10)
        btn_action.grid(column=2, row=self.row_current, ipadx=self.row_padding)
        self.row_current+=1

    def set_home(self):
        """This function sets up the home screen for the staffer"""
        self.window.title(ld.get_text_from_dict(self.language, self.staff_id))
        staff_name = Label(self.window, text=self.staff_name, font=data.get_large_font())
        staff_name.grid(column=0, row=0)
        self.add_column_headers()

    def add_column_headers(self):
        """This function adds the headers for the tasks in the home screen (name     task)"""
        label_name = Label(self.window, text=ld.get_text_from_dict(self.language, '~1'), font=data.medium_font)
        label_name.grid(column=1, row=self.row_current, ipady=self.row_padding)
        label_event = Label(self.window, text=ld.get_text_from_dict(self.language, '~33'), font=data.get_medium_font())
        label_event.grid(column=2, row=self.row_current, ipadx=self.column_padding, ipady=self.row_padding)
        self.row_current += 1

    def add_person_to_tasks(self, person_id):
        """This function adds the name of a person who needs to be processed by the staffer
        :param person_id: identification number of the person
        :type person_id: int
        """
        name = data.get_data('pdata', 2, int(person_id), 9, '~1')[0][11]
        label_name = Label(self.window, text=name, font=data.medium_font)
        label_name.grid(column=1, row=self.row_current, ipady=self.row_padding)

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
                self.add_label(item[1], person_id)
            elif item[0] == 'PersonHeader':
                self.add_person_header(person_id)
            elif item[0] == 'TaskHeader':
                self.add_task_header(task_id)
            elif item[0] == 'ModifyEntry':
                self.add_entry_with_text(item[1], person_id)
            elif item[0] == 'EmptyEntry':
                self.add_entry(item[1])
            elif item[0] == 'DropDown':
                self.add_drop_down(item[1:])
            elif item[0] == 'CheckBoxes':
                self.add_check_boxes(item[1:])
            elif item[0] == 'Button':
                self.add_button_submit(item[1], token)

    def clear_window(self):
        """This function clears the window that it is given allowing it to be a blank canvas before the window
        is populated with new data
        """
        for widget in self.window.winfo_children():
            widget.destroy()

    def add_label(self, value, person_id):
        """this function adds a label to a given window
        :param person_id:  identification number of person (11, or 12) for (tina, tony)
        :type person_id: int
        :param value: a dictionary reference to a value that needs to be written in the form a label to the screen
        :type value: str
        """
        lbl = Label(self.window, text=ld.get_text_from_dict(self.language, value) + ': ', font=data.medium_font)
        lbl.grid(row=self.task_row, column=0, ipady=self.row_padding, sticky='W')
        dict_token = data.get_data('pdata', 2, int(person_id), 9, value)[0].__getitem__(11)

        lbl_info = Label(self.window, text=ld.get_text_from_dict(self.language, dict_token))

        lbl_info.grid(row=self.task_row, column=1, ipady=self.row_padding, sticky='W')
        self.task_row += 1

    def add_drop_down(self, value):
        """this method adds a drop down menu to a given window
        :param value: a dictionary reference to a value that needs to be written in the form a label to the screen
        :type value: str
        """
        drop_down_lbl = value[0]
        list_call = value[1]
        lbl = Label(self.window, text=ld.get_text_from_dict(self.language, drop_down_lbl) + ': ', font=data.medium_font)
        lbl.grid(row=self.task_row, column=0, ipady=self.row_padding, sticky='W')
        choices = data.get_data('choices').get(list_call)
        choices_formatted = []
        choice_dict = {}
        for choice in choices:
            choices_formatted.append(ld.get_text_from_dict(self.language, choice[0]))
            choice_dict[ld.get_text_from_dict(self.language, choice[0])] = choice[0]

        option = StringVar(self.window)
        drop_down = OptionMenu(self.window, option, *choices_formatted)
        drop_down.grid(row=self.task_row, column=1, sticky='W')

        self.widgets.append((drop_down_lbl, option, choice_dict))
        self.task_row += 1

    def add_button_submit(self, value, token):
        """this method adds a submit button to a given window
        :param value: a dictionary reference to a value that needs to be written in the form a label to the screen
        :type value: str
        """
        btn_submit = Button(self.window, text=ld.get_text_from_dict(self.language, value),
                            command=lambda: self.submit_btn_listener(token),
                            fg="black", bg="gray", height=1, width=10)
        btn_submit.grid(row=self.task_row + 5, column=0, sticky='S')
        self.task_row += 1

    def submit_btn_listener(self, token):
        """an action listener for the submit button.  As it stands, it only takes the staffer back to their home screen
        but this is where the addition of data to pdata and the log will go
        """
        self.manage_widgets()
        self.widgets.clear()
        self.clear_window()
        self.add_to_log()
        self.value_holder.clear()
        self.token = None
        # self.at_home = True   FOR USE WITH POLLING PEO_Q
        # self.time_label.config(text = self.simulate.get_time().__str__())
        self.at_home = True
        self.home.return_data(token)
        self.set_home()

    def add_to_log(self):
        """This function adds the data that will be sent back to the protocol manager to the log window
        print statement is so you can see how the actual value looks in the program not just the log printed version"""
        if len(self.value_holder[2]) > 0:
            print(self.value_holder)
            Label(self.log_window, text=self.value_holder, font=data.medium_font).pack()

    def add_check_boxes(self, value):
        """This method adds a check box to the given window.  As it stands it only places the header for the check
        box but check box functionality will be added in the next update
        :param value: a dictionary reference to a value that needs to be written in the form a label to the screen
        and a str that references the list to be called from data.py
        :type value: list
        """
        cb_label = value[0]
        list_call = value[1]
        lbl = Label(self.window, text=ld.get_text_from_dict(self.language, cb_label) + ': ', font=data.medium_font)
        lbl.grid(row=self.task_row, column=0, ipady=self.row_padding, sticky='W')
        cb_values = data.get_data('choices').get(list_call)
        for val in cb_values:
            test = ld.get_text_from_dict(self.language, val[0])
            checked = IntVar()
            box = Checkbutton(self.window, text=test, variable=checked,
                              onvalue=1, offvalue=0)
            self.widgets.append((value, [checked, val[0]]))
            box.grid(row=self.task_row, column=1, sticky='W')
            self.task_row += 1
        self.task_row += 1

    def add_entry(self, value):
        """This method adds an entry to the given window.  As it stands it only places the header for the entry box
         but entry box functionality will be added in the next update
        :param value: a dictionary reference to a value that needs to be written in the form a label to the screen
        :type value: str
        """
        lbl = Label(self.window, text=ld.get_text_from_dict(self.language, value) + ': ', font=data.medium_font)
        lbl.grid(row=self.task_row, column=0, ipady=self.row_padding, sticky='W')
        text_entered = StringVar()
        entry_box = Entry(self.window, textvariable=text_entered)
        self.widgets.append((value, entry_box))
        entry_box.grid(row=self.task_row, column=1, sticky='W')
        self.task_row += 1

    def add_entry_with_text(self, value, person_id):
        """This method adds an entry with text prefilled to the given window.  As it stands it only places the header for the entry box
         but entry box functionality will be added in the next update
        :param person_id: identification number of the person in question
        :type person_id: int
        :param value: a dictionary reference to a value that needs to be written in the form a label to the screen
        :type value: str
        """
        phone_number = data.get_data('pdata', 2, int(person_id), 9, value)[0].__getitem__(11)
        lbl = Label(self.window, text=ld.get_text_from_dict(self.language, value) + ': ', font=data.medium_font)
        lbl.grid(row=self.task_row, column=0, ipady=self.row_padding, sticky='W')
        text_entered = StringVar()
        entry_box = Entry(self.window, textvariable=text_entered)
        entry_box.insert(0, phone_number)
        self.widgets.append((value, entry_box))
        entry_box.grid(row=self.task_row, column=1, sticky='W')
        self.task_row += 1

    def add_task_header(self, task_id):
        """This method adds the task header of the staffer to the display window. After adding, I'm not sure
        this is something we really need but could be useful in the future
        :param task_id: the ~vocab reference of the task that must be completed by the staffer
        :type task_id: str"""
        task = ld.get_text_from_dict(self.language, task_id)
        task_lbl = Label(self.window, text=task, font=data.get_medium_font())
        task_lbl.grid(row=self.task_row, column=0, columnspan=2, sticky='W')
        self.task_row += 1

    def add_person_header(self, person_id):
        """This method adds the person header to the given window based on the id number of the person given to the
        method.
        :param person_id: the identification number of the person being processed used to intake their data
        :type person_id: int
        """
        person_data = data.get_data('pdata', 2, person_id)
        name = person_data[0].__getitem__(11)
        sex = ld.get_text_from_dict(self.language, person_data[1].__getitem__(11))
        age = person_data[2].__getitem__(11).__str__()
        name_lbl = Label(self.window, text=name, font=data.medium_font)
        sex_lbl = Label(self.window, text=sex, font=data.medium_font)
        age_lbl = Label(self.window, text=age, font=data.medium_font)

        name_lbl.grid(row=self.task_row, column=0, sticky='W')
        sex_lbl.grid(row=self.task_row, column=1, sticky='W')
        age_lbl.grid(row=self.task_row, column=2, sticky='W')
        self.task_row += 1

    def add_value(self, key, value):
        """This function adds a key value pair to the stored information retrieved from the widgets in the task screen
        :param key: the key corresponding to a dictionary reference in language_dictionary
        :type key: str
        :param value: the value retrieved from the widget in the task screen
        :type value: int or str"""
        self.value_holder[2].append({'k': key, 'v': value})

    def manage_widgets(self):
        """This function loops through the widgets stored in the task screen for the staffer.  It's job is to retrieve
        the data from the widgets so they can be passed back to the protocol manage and currently prints to the log
        window.  Added exceptions for when there are no values given so empty lists are not added or displayed"""
        self.value_holder.append(self.token)
        self.value_holder.append(datetime.datetime.now().timestamp())
        self.value_holder.append([])
        for widget in self.widgets:
            if len(widget) == 3:
                if len(widget[1].get()) > 0:
                    self.add_value(widget[0], widget[2].get(widget[1].get()))

            elif widget[0][0] == '~18':  # if it is a checkbox input
                if widget[1][0].get() == 1:
                    self.add_value(widget[0][0], widget[1][1])
            else:
                if len(widget[1].get()) > 0:
                    self.add_value(widget[0], widget[1].get())
