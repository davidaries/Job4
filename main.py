"""
This class is in charge of the main construction of the GUI for Job2
This involves the creation of multiple windows
There is a primary window for handling pausing, unpausing and ending the program
There is a timer window, which increments every second
Finally, there is a log window used for writing down the arrivals and departures of staffers

:param base_language: Sets base_language for the program to english (~101) or spanish (~102)
:type base_language: str
:param root: is an instance of tkinter creating the main window for program.  root holds the primary pause, unpause,
    and end buttons to interact with the timer (pausing and unpausing) as well as ending the program
:type root: tkinter class reference

:param time_window: creates a separate window used for displaying the current running time of the application.
this is formatted in HOURS:MINUTES:SECONDS as a format
:type time_window: tkinter window
:param time_now: is a label inside packed inside of the time_window used to display current running time
:type time_now: Label

:param log_window: creates a window to write a time stamped arrival or departure of a staffer to the log
:type log_window: tkinter window
:param label_name: is the header of the name column of the log window
:type label_name: Label
:param label_event: is the header of the event column of the log window
:type label_event: Label
:param label_time: is the header of the time column of the log window
:type label_time: Label

:param btn_pause: this is a button contains the text 'pause' in the appropriate language based on
    base_language as defined above.  It connects to the action listener clicked_pause to handle what
    happens after the button is clicked
:type btn_pause: Button
:param btn_unpause: this is a button contains the text 'unpause' in the appropriate language based on
    base_language as defined above.  It connects to the action listener clicked_unpause to handle what
    happens after the button is clicked
:type btn_pause: Button
:param btn_end: this is a button contains the text 'end' in the appropriate language based on
    base_language as defined above.  It connects to the action listener clicked_end to handle what
    happens after the button is clicked
:type btn_end: Button
"""
import time
from tkinter import *
import staff_manager as sm
import internal_timer as in_time
import tkinter.font as tkFont
import language_dictionary as ld
import data
import controller
from home_screen import home_screen

base_language = data.get_data('language_preference')

root = Tk()

data.create_fonts(root) # data.create_fonts(root) creates the fonts to be used in the program

root.title(ld.get_text_from_dict(base_language, '~11'))  # title for window
root.geometry('302x100+0+0')  # main window geometry
time_lbl = Label(root, text= "test", font = 'Helvetica 18 bold')
time_lbl.pack()
""""""
# pd = [[111, 2, 3], [111, 4, 5], [222, 6, 7], [222, 8, 9]] # the first field (offset 0) is the person id.
# persons = [111, 222]
# person_dict = {}
#
# for p in persons:
#     person_dict[p] = [[pd[1], pd[2]] for pd in pd if pd[0] == p]
#
# print(person_dict.get(111))
# print(person_dict.get(222))
# TIME WINDOW NOT NEEDED FOR JOB 3
# time_window = Toplevel(root)
# time_window.title(ld.get_text_from_dict(base_language, '~12'))
# time_window.geometry("200x200+600+0")
# time_now = Label(time_window, text=" ", font=data.get_large_font())
# time_now.pack()
#
# in_time.__init__(root, time_now)

"""passes the main program window pointer and label for timer to be used in internal_timer.py"""

# create Log Window
log_window = Toplevel(root)
log_window.title(ld.get_text_from_dict(base_language, '~13'))
log_window.geometry("600x300+0+500")

control = controller
staffers_home = home_screen(root, log_window,control)

staffers_home.manage_staff_main_screen(staffers_home)
control.start(staffers_home,root,time_lbl)


# creation of labels for the Log Window not needed for JOB 3
logPadding = 25
# label_name = Label(log_window, text=ld.get_text_from_dict(base_language, '~1'), font=data.get_large_font())
# label_name.grid(column=1, row=1, ipadx=logPadding)
# label_event = Label(log_window, text=ld.get_text_from_dict(base_language, '~9'), font=data.get_large_font())
# label_event.grid(column=2, row=1, ipadx=logPadding)
# label_time = Label(log_window, text=ld.get_text_from_dict(base_language, '~10'), font=data.get_large_font())
# label_time.grid(column=3, row=1, ipadx=logPadding)

sm.__init__(root, log_window)


"""passes a reference to the main GUI root and the log window to be used in staff_manager.py"""


# button action listeners
#def clicked_pause():
"""This is an action listener for the button defined below btn_pause.  It is in charge of handling
        the pausing of the programs internal timer by calling the pause_time function in internal_timer.py"""
    #in_time.pause_time()


#def clicked_unpause():
"""This is an action listener for the button defined below btn_un_pause.  It is in charge of handling
        the pausing of the programs internal timer by calling the resume_time function in internal_timer.py"""
    #in_time.resume_time()


#def clicked_end():
"""This is an action listener for the button defined below btn_end.  It is in charge of destroying the
        root of the program and thus ending program execution"""
    #root.destroy()

"""
btn_pause = Button(root, text=ld.get_text_from_dict(base_language, '~6'), fg="black", bg="gray", command=clicked_pause,
                   height=1, width=13)
btn_unpause = Button(root, text=ld.get_text_from_dict(base_language, '~7'), fg="black", bg="gray",
                     command=clicked_unpause, height=1, width=13)
btn_end = Button(root, text=ld.get_text_from_dict(base_language, '~8'), fg="black", bg="gray", command=clicked_end,
                 height=1, width=13)
"""
"""the following three lines of code add the buttons btn_pause, btn_unpause, btn_end in a grid format to root (the 
    primary window of the application

btn_pause.grid(column=1, row=1)
btn_unpause.grid(column=2, row=1)
btn_end.grid(column=3, row=1)
"""
#in_time.manage_time()
"""in_time.manage_time(): starts the internal timer in the application"""

root.mainloop()
"""root.mainloop(): begins the visual execution of the program"""
