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
from tkinter import *
import language_dictionary as ld
import controller
from home_screen import home_screen
from system_time import system_time

base_language = '~101'

root = Tk()

root.title(ld.get_text_from_dict(base_language, '~11'))  # title for window
root.geometry('430x100+0+0')  # main window geometry
time_lbl = Label(root, text= "test", font = 'Helvetica 18 bold')
time_lbl.grid(row=0,column=1)

# create Log Window
log_window = Toplevel(root)
log_window.title(ld.get_text_from_dict(base_language, '~13'))
log_window.geometry("600x300+0+500")
log_window.withdraw()

timer = system_time(root, time_lbl)
timer.clock()

control = controller
staffers_home = home_screen(root, log_window,control, timer)
staffers_home.add_home(staffers_home)
control.set_global_timer(timer)
control.start(root)

btn_pause = Button(root, text=ld.get_text_from_dict('~101', '~6'), fg="black", bg="gray",
                   command= lambda: timer.stop_clock(True),
                   height=1, width=13)
btn_unpause = Button(root, text=ld.get_text_from_dict('~101', '~7'), fg="black", bg="gray",
                     command= lambda: timer.stop_clock(False), height=1, width=13)
btn_sum = Button(root, text='Current Status', fg="black", bg="gray",
                     command= control.summary, height=1, width=13)
btn_login_page = Button(root, text = 'login', fg="black", bg="gray",
                        command=staffers_home.login_screen, height=1, width=13)
test = Button(root, text = 'test', fg="black", bg="gray",
                        command=staffers_home.login_all, height=1, width=13)
btn_pause.grid(column=0, row=1)
btn_sum.grid(column=1,row=1)
btn_unpause.grid(column=2, row=1)
btn_login_page.grid(column = 0, row =2)
test.grid(column = 2, row =2)
# creation of labels for the Log Window not needed for JOB 3
logPadding = 25


root.mainloop()
"""root.mainloop(): begins the visual execution of the program"""
