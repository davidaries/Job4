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
root = None

global pause, pause_time, current_time
pause = False


def stop_clock(val):
    global pause, pause_time
    pause = val
    pause_time = time.perf_counter()

def get_time():
    return time.mktime(current_time.timetuple())

def check_entrant():
    if current_time.minute < 10:
        time_str = ("%s:0%s" % (current_time.hour, current_time.minute))
    else:
        time_str = ("%s:%s" % (current_time.hour, current_time.minute))
    for ent in data.entrants:
        if time_str == ent[0]:
            pe_ins_unsol.append(['ip01', datetime.datetime.now().timestamp(),
                                 {'person': ent[1], 'entity': None, 'actor': '~self', 'call': [['p0001', 1, 3]]}])


def start(staffers_home, rt, time_lbl):
    global pause_time, current_time
    time_label = time_lbl
    root = rt

    # START - clock function  ##########################################################
    opening_time = datetime.datetime(2021, 1, 9, 7, 0, 0)
    current_time = opening_time
    pause_time = opening_time

    def clock():
        global current_time
        if not pause:
            current_time += datetime.timedelta(seconds=60)
            time_label.config(text=str(current_time))
            check_entrant()

    # ## END - clock function  ##########################################################

    # START - simulation ##########################################################
    loop = 0
    sim_start_time = (datetime.datetime.now().timestamp())

    def simulate(loop):
        if not pause:
            loop += 1
            # Now let's run the protocol engine
            clock()
            pdata_appendums, adat_appendums = pe.protocol_engine(pe_ins_sol, pe_waits, pe_ins_unsol, pe_outs)
            for i in pdata_appendums:
                pdata.append(i)
            if adat_appendums:
                for j in adat_appendums:
                    print(j)
                    print(data.adat[j[0]])
                    try:
                        data.adat[j[0]][j[1]].append(j[2])
                    except:
                        data.adat[j[0]][j[1]] = [j[2]]
            clock()
        root.after(1000, lambda: simulate(loop))
    #root.after(1000, lambda: simulate(loop))
    simulate(loop)

# ### END - simulation ##########################################################
def poll_tasks(device_id):
    return pe_outs.get(str(device_id))


def return_completion(pe_in, data_return):
    if pe_in:
        pe_ins_sol.append([pe_in, get_time(), {'data': data_return}])
    print(pe_ins_sol)


# START - PRINTING FINAL STATUS - ONLY FOR REVIEW/TROUBLESHOOTING ##########
def summary():
    print('\n========= Summary data at end of program =========================================================')
    print('==============pe_ins_sol data====================')
    print(pe_ins_sol)
    print('==============pe_ins_unsol data====================')
    print(pe_ins_unsol)
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

    # print('\npe_ins =', pe_ins_sol)
    # for z in pe_ins_sol:
    #     print(z, pe_ins_sol[z])

# ### END - PRINTING FINAL STATUS - ONLY FOR REVIEW/TROUBLESHOOTING ##########
