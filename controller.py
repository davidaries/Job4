# controller.py
import PEv1_data as data
import datetime
import time
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
persons = ['pers101', 'pers102', 'pers103', 'pers104', 'pers105']

time_label = None
global timer


def set_global_timer(timer_ref):
    global timer
    timer = timer_ref
    pe.set_sim_time(timer_ref)


def check_entrant():
    global timer
    time_str= timer.get_formatted_time().strftime("%H:%M")
    for ent in data.entrants:
        if time_str == ent[0]:
            pe_ins_unsol.append(['ip01', timer.get_time_stamp(),
                                 {'person': ent[1], 'entity': None, 'actor': '~self', 'call': [['p0001', 1, 3]]}])


def start(root):
    # START - simulation ##########################################################
    def simulate():
        if not timer.pause():
            # Now let's run the protocol engine
            pdata_appendums, adat_appendums = pe.protocol_engine(pe_ins_sol, pe_waits, pe_ins_unsol, pe_outs)
            for i in pdata_appendums:
                pdata.append(i)
            if adat_appendums:
                for j in adat_appendums:
                    try:
                        data.adat[j[0]][j[1]].append(j[2])
                    except:
                        data.adat[j[0]][j[1]] = [j[2]]
            check_entrant()
        root.after(1000, simulate)
    simulate()

# ### END - simulation ##########################################################
def poll_tasks(device_id):
    return pe_outs.get(str(device_id))


def return_completion(pe_in, data_return):
    global timer
    if pe_in:
        pe_ins_sol.append([pe_in, timer.get_time_stamp(), {'data': data_return}])


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
