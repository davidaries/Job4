# controller.py

import datetime
import time
import home_screen
from tkinter import *
import pe

# START - setting things up ##########################################################
# Some empty data fields to be used
pdata = []
pe_ins_sol = []  # protocol engine inputs
pe_ins_unsol = []
pe_outs = {}  # protocol engine outputs
pe_waits = {}  # protocol engine waits
pe_outs['123'] = {}  # when a staff member signs in with a device the device needs an empty dictionary
pe_outs['234'] = {}  # these four pe_outs rows will go away when we have a staff sign in process
pe_outs['345'] = {}
pe_outs['456'] = {}

# creating two persons showing up - so we have something to run
persons = ['11', '12']

time_label = None
root = None


def start(staffers_home, rt,time_lbl):
    time_label = time_lbl
    root = rt
    for i in persons:
        pe_ins_unsol.append(['ip01', datetime.datetime.now().timestamp(),
                             {'person': i, 'entity': None, 'actor': '~self', 'call': [['p0001', 1, 3]]}])

    # ## END - setting things up ##########################################################

    # START - clock function  ##########################################################
    opening_time = 1609340400

    def clock():
        multiplier = 100
        current_time = opening_time + round((datetime.datetime.now().timestamp() - sim_start_time) * multiplier)
        print(datetime.datetime.fromtimestamp(current_time))
        time_lbl.config(text=str(datetime.datetime.fromtimestamp(current_time)))

    # ## END - clock function  ##########################################################

    # START - simulation ##########################################################
    loop = 0
    sim_start_time = (datetime.datetime.now().timestamp())

    def simulate(loop):

        # while loop < 10:  # alternative to the next line, keeps things going even if no pe_ins_unsol or pe_ins_sol
        loop += 1
        time.sleep(.1)

        # Now let's run the protocol engine
        print('\n========== RUNNING PROTOCOL ENGINE ================')
        print('loop = ', loop)
        clock()
        pdata_appendums = pe.protocol_engine(pe_ins_sol, pe_waits, pe_ins_unsol, pe_outs)
        for i in pdata_appendums:
            pdata.append(i)

        # Now let's run the protocol engine
        print('\n========== USER INTERFACE ================')
        print('loop = ', loop)
        clock()
        staffers_home.user_interface(pe_outs)
        if loop == 25:
            summary()
        if loop <25:
            root.after(1000, lambda: simulate(loop))


    simulate(loop)


# ### END - simulation ##########################################################

def return_completion(pe_in,time):
    print(pe_outs['123'])
    if pe_in:
        pe_ins_sol.append([pe_in,time,{'text': 'Great Stuff!'}])


# START - PRINTING FINAL STATUS - ONLY FOR REVIEW/TROUBLESHOOTING ##########
def summary():
    print('\n========= Summary data at end of program =========================================================')

    print('\npdata =', pdata)
    for h in pdata:
        print(h)

    print('\npe_outs =', pe_outs)
    dev_outs = pe_outs.keys()
    for i in pe_outs:
        print('device_out = ', i)
        for ii in pe_outs[i]:
            print('  ', ii, pe_outs[i][ii])

    print('\npe_waits =', pe_waits)
    for j in pe_waits:
        print(j, pe_waits[j])

# ### END - PRINTING FINAL STATUS - ONLY FOR REVIEW/TROUBLESHOOTING ##########
