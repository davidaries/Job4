import language_dictionary as ld
from tkinter import *
from tkinter import font as tk_font
import PEv1_data as pe_data


class login_manager:
    def __init__(self, root, language, home, window):
        self.root = root
        self.language = language
        self.home = home
        self.window = window
        self.medium_font = tk_font.Font(root=root.master, family='Helvetica', size=10, weight=tk_font.BOLD)
        self.larger_font = tk_font.Font(root=root.master, family='Helvetica', size=10, weight=tk_font.BOLD)
        self.column_padding = 80
        self.row_padding = 12
        self.row_current = 2
        self.task_row = 0
        self.login_widgets = []

    def add_entry_id(self):
        """This method adds an entry to the given window.  As it stands it only places the header for the entry box
         but entry box functionality will be added in the next update
        :param value: a dictionary reference to a value that needs to be written in the form a label to the screen
        :type value: str
        """
        lbl = Label(self.window, text=ld.get_text_from_dict(self.language, '~42') + ': ', font=self.medium_font)
        lbl.grid(row=self.task_row, column=0, ipady=self.row_padding, sticky='W')
        text_entered = StringVar()
        entry_box = Entry(self.window, textvariable=text_entered)
        self.login_widgets.append(('~42', entry_box))
        entry_box.grid(row=self.task_row, column=1, sticky='W')
        self.task_row += 1

    def add_entry_password(self):
        """This method adds an entry to the given window.  As it stands it only places the header for the entry box
         but entry box functionality will be added in the next update
        :param value: a dictionary reference to a value that needs to be written in the form a label to the screen
        :type value: str
        """
        lbl = Label(self.window, text=ld.get_text_from_dict(self.language, '~43') + ': ', font=self.medium_font)
        lbl.grid(row=self.task_row, column=0, ipady=self.row_padding, sticky='W')
        text_entered = StringVar()
        entry_box = Entry(self.window, textvariable=text_entered)
        entry_box.config(show="*")
        self.login_widgets.append(('~42', entry_box))
        entry_box.grid(row=self.task_row, column=1, sticky='W')
        self.task_row += 1

    def login_button(self):
        btn_submit = Button(self.window, text=ld.get_text_from_dict(self.language, '~20'),
                            command=lambda: self.login_button_listener(),
                            fg="black", bg="gray", height=1, width=10)
        btn_submit.grid(row=self.task_row, column=0, sticky='S')

    def login_button_listener(self):
        login_info = []
        for entry in self.login_widgets:
            login_info.append(entry[1].get())
        try:
            if pe_data.staffer_login_info.get(login_info[0])[0] == login_info[1]:
                if not pe_data.staffer_login_info.get(login_info[0])[1]:
                    self.successful_login(login_info[0], self.window)
                else:
                    self.unsuccessful_login("USER LOGGED IN ALREADY")
            else:
                self.unsuccessful_login("INVALID PASSWORD")
        except:
            self.unsuccessful_login("INVALID LOGIN")

    def unsuccessful_login(self, error):
        Label(self.window, text=error, font=self.larger_font).grid(row=self.task_row + 1, column=1)
        self.root.after(1000, self.reset_login)

    def reset_login(self):
        self.login_widgets.clear()
        self.clear_window()
        self.add_entry_id()
        self.add_entry_password()
        self.login_button()

    def successful_login(self, staffer_id, window):
        pe_data.staffer_login_info.get(staffer_id).__setitem__(1, True)
        self.home.check_login(staffer_id, window)

    def clear_window(self):
        """This function clears the window that it is given allowing it to be a blank canvas before the window
        is populated with new data
        """
        for widget in self.window.winfo_children():
            widget.destroy()
