import language_dictionary as ld
from tkinter import *
from tkinter import font as tk_font
import PEv1_data as pe_data
import query


class widgets:

    def __init__(self, root, language, window=None, home=None):
        self.language = language
        self.home = home
        self.window = window
        self.medium_font = tk_font.Font(root=root.master, family='Helvetica', size=10, weight=tk_font.BOLD)
        self.larger_font = tk_font.Font(root=root.master, family='Helvetica', size=10, weight=tk_font.BOLD)
        self.column_padding = 80
        self.row_padding = 12
        self.row_current = 2
        self.task_row = 0
        self.widgets = []
        self.login_widgets = []

    def return_widget_data(self):
        return self.widgets

    def add_label(self, value, person_id):
        """this function adds a label to a given window
        :param person_id:  identification number of person (11, or 12) for (tina, tony)
        :type person_id: int
        :param value: a dictionary reference to a value that needs to be written in the form a label to the screen
        :type value: str
        """
        print(value)
        lbl = Label(self.window, text=ld.get_text_from_dict(self.language, value) + ': ', font=self.medium_font)
        lbl.grid(row=self.task_row, column=0, ipady=self.row_padding, sticky='W')
        lbl_val = query.adat_person_key(person_id, value)[1]
        # lbl_val = query.query_adat(person_id, [[value, ['last']]])[0][2]
        lbl_info = Label(self.window, text=ld.get_text_from_dict(self.language, lbl_val))

        lbl_info.grid(row=self.task_row, column=1, ipady=self.row_padding, sticky='W')
        self.task_row += 1

    def add_drop_down(self, value):
        """this method adds a drop down menu to a given window
        :param value: a dictionary reference to a value that needs to be written in the form a label to the screen
        :type value: str
        """
        drop_down_lbl = value[0]
        list_call = value[1]
        lbl = Label(self.window, text=ld.get_text_from_dict(self.language, drop_down_lbl) + ': ', font=self.medium_font)
        lbl.grid(row=self.task_row, column=0, ipady=self.row_padding, sticky='W')
        choices = pe_data.choices.get(list_call)
        choices_formatted = []
        choice_dict = {}
        for choice in choices:  # short list
            if choice[1]:
                choices_formatted.append(ld.get_text_from_dict(self.language, choice[0]))
                choice_dict[ld.get_text_from_dict(self.language, choice[0])] = choice[0]
        if list_call == 'c102':
            choices_formatted.append('_____________')
        for choice in choices:  # long list
            if list_call == 'c102':
                choices_formatted.append(ld.get_text_from_dict(self.language, choice[0]))
                choice_dict[ld.get_text_from_dict(self.language, choice[0])] = choice[0]
        option = StringVar(self.window)
        drop_down = OptionMenu(self.window, option, *choices_formatted)
        drop_down.grid(row=self.task_row, column=1, sticky='W')

        self.widgets.append((drop_down_lbl, option, choice_dict))
        self.task_row += 1

    def add_check_boxes(self, value):
        """This method adds a check box to the given window.  As it stands it only places the header for the check
        box but check box functionality will be added in the next update
        :param value: a dictionary reference to a value that needs to be written in the form a label to the screen
        and a str that references the list to be called from data.py
        :type value: list
        """
        cb_label = value[0]
        list_call = value[1]
        lbl = Label(self.window, text=ld.get_text_from_dict(self.language, cb_label) + ': ', font=self.medium_font)
        lbl.grid(row=self.task_row, column=0, ipady=self.row_padding, sticky='W')
        cb_values = pe_data.choices.get(list_call)
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
        lbl = Label(self.window, text=ld.get_text_from_dict(self.language, value) + ': ', font=self.medium_font)
        lbl.grid(row=self.task_row, column=0, ipady=self.row_padding, sticky='W')
        text_entered = Variable
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
        phone_number = query.adat_person_key(person_id, '~16')[1]
        lbl = Label(self.window, text=ld.get_text_from_dict(self.language, value) + ': ', font=self.medium_font)
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
        task_lbl = Label(self.window, text=task, font=self.medium_font)
        task_lbl.grid(row=self.task_row, column=0, columnspan=2, sticky='W')
        self.task_row += 1

    def add_person_header(self, person_id):
        """This method adds the person header to the given window based on the id number of the person given to the
        method.
        :param person_id: the identification number of the person being processed used to intake their data
        :type person_id: int
        """

        name = query.adat_person_key(person_id, '~1')[1]
        sex = query.adat_person_key(person_id, '~14')[1]
        sex = ld.get_text_from_dict(self.language, sex)
        age = query.adat_person_key(person_id, '~15')[1]
        name_lbl = Label(self.window, text=name, font=self.medium_font)
        sex_lbl = Label(self.window, text=sex, font=self.medium_font)
        age_lbl = Label(self.window, text=age, font=self.medium_font)

        name_lbl.grid(row=self.task_row, column=0, sticky='W')
        sex_lbl.grid(row=self.task_row, column=1, sticky='W')
        age_lbl.grid(row=self.task_row, column=2, sticky='W')
        self.task_row += 1

    def clear_widget_data(self):
        self.widgets.clear()