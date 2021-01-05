from tkinter import *
import internal_timer as in_time
import language_dictionary as ld
import data
#import time as tm

log_row = 1

log = None
root = None
popup_spacer = 140


# converts and returns the counter time in format HR:MIN:SEC


def __init__(master, log_window):
    """constructor method
    :param master: establishes a pointer to the root of the program
    :type master: reference to Tk class
    :param log_window: reference to a tkinter window
    :type log_window: tkinter window
    """
    global log, root
    log = log_window
    root = master


# function for managing staff input into the log based on real time
def staff_entrance():
    """manages the creation of a popup window for a staff member when they arrive
    Does this by obtaining a list of the staffers from data.py, looping through the list and if a staffer is set
    to enter at the current time a staff member pop is created
    """
    staffers = data.get_staffers_list()
    entering_staff = [staffer for staffer in staffers if staffer[1] == in_time.time_count]
    if len(entering_staff) > 0:
        for member in entering_staff:
            create_staff_popup(member)


def write_person_event(person, action):
    """This method manages the writing of a staff member's event to the log window.  This is done by adding the staff
    member's name and the formatted time of ther arrival and departure and adding it to the appropriate row/column
    in the log window
    :param person: person contains the list of information about the person being written to the log entry
    :type person: list
    :param action: action variable contains whether the staff memeber is arriving or departing
    :type action: str"""
    global log_row
    lbl_log_output_name = Label(log, text=person[0])
    lbl_log_output_name.grid(column=1, row=1 + log_row)
    lbl_log_output_visit = Label(log, text=action)
    lbl_log_output_visit.grid(column=2, row=1 + log_row)
    lbl_log_output_time = Label(log, text=in_time.get_formatted_time())
    lbl_log_output_time.grid(column=3, row=1 + log_row)
    log_row += 1


def create_staff_popup(staff_data):
    """this method creates a pop up window for the staff member as they arrive"""
    global popup_spacer, log, root
    person_data = data.get_next_person()
    language = staff_data[3]

    def clicked_exit():
        """function to handle the clicking of exit and close a window presented for the staff member and write their
        departure to the log.  Window distruction is done by calling the .destroy() function for the root of that window"""
        write_person_event(staff_data, 'depart')  # write event to the log
        person_popup.destroy()

    def manage_non_laggard():
        """a method for handling staff members marked as laggards.  In the current iteration of this method,
        clicked_exit is called after a wait time of 3 seconds.  As of now, it does not distinguish whether the timer
        is or is not currently running at the time of exiting """
        root.after(3000,clicked_exit)

    # create the popup window for a person
    person_popup = Toplevel(root)
    person_popup.title(staff_data[0])
    person_popup.geometry("200x110+0+" + popup_spacer.__str__())
    greeting = Label(person_popup, text=ld.get_text_from_dict(language, '~4'))
    greeting.pack()
    person_name = Label(person_popup, text=ld.get_text_from_dict(language, '~1') + ': ' + person_data[0])
    person_name.pack()
    person_diagnosis = Label(person_popup,
                             text=ld.get_text_from_dict(language, '~2') + ': ' + ld.get_text_from_dict(language,
                                                                                                       person_data[1]))
    person_diagnosis.pack()
    popup_spacer += 160

    # create an exit button
    btn_exit = Button(person_popup, text=ld.get_text_from_dict(language, '~3'), fg="black", bg="gray",
                      command=clicked_exit, height=1, width=10)
    btn_exit.pack(side=BOTTOM)
    write_person_event(staff_data, 'arrive')
    # handle laggard status with a new function
    if not staff_data[2]:
        manage_non_laggard()
