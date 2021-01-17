# pe.py

import datetime
import random
import PEv1_data as PEd
import get_responsible_staff as grs

global sim_time


def set_sim_time(s_time):
    """This function creates a reference to the simulation time module used for reporting current simulatio time
    :param s_time: a reference to the system_time module
    :type s_time: module"""
    global sim_time
    sim_time = s_time


# START - function to process the calls a pdata row holds - this is called by (and is part of) PE ############
def process_calls(calls, pdata_appendum, pe_outs, pe_waits):
    for protostep in calls:  # calls can have more than one protostep, so we need to cycle through them
        pe_out, pe_wait = two_writes(pdata_appendum, protostep)  # we call two_writes to get pe_out and pe_wait
        pe_outs[pe_out[0]][pe_out[1]] = pe_out[2]    # this adds the new pe_out to pe_outs
        if pe_wait[1]:    # this if because without it when a protocol ended we'd get a empty pe_wait written anyway
            pe_waits[pe_wait[0]] = pe_wait[1]        # this adds the new pe_wait to pe_waits
# ### END - function to process the calls a pdata row holds - this is called by (and is part of) PE ############


# START - function to create a pe_out and a pe_wait - called by process_calls and is part of PE ################
def two_writes(pdata_appendum, protostep):
    global sim_time
    # for reference pdata_appendum WAS = [pdatm[0], meta_pdatm[1], person[2], entity[3], caller[4], protocol[5], step[6], thread[7], record_dts[8], datas_write[9], actor[10]]
    # for reference pdata_appendum NOW IS = [pdatm[0], person[1], entity[2], caller[3], protocol[4], step[5], thread[6], record_dts[7], datas[8]]
    protocol, step, priority = protostep[0], protostep[1], protostep[2]
    token = random.randint(1000000000000001, 9999999999999999)   # the token is used later to match a pe_in (from the UI) with its corresponding pe_wait
    # the next fields are read directly from pdata_addendum
    caller = pdata_appendum[0]
    person = pdata_appendum[1]
    entity = pdata_appendum[2]
    thread = pdata_appendum[6]
    if step == 1:   # if this is the first step in a protocol it needs a new thread number
        thread = random.randint(100001, 999999)
    # the next four are from the protocol specification for that step
    task = PEd.protocols[protocol][step][1]
    task_type = PEd.protocols[protocol][step][2]
    spec = PEd.protocols[protocol][step][3]
    flow = PEd.protocols[protocol][step][5]
    # then a few more loose fields
    time_posted = sim_time.get_time_stamp()
    time_reposted = None    # placeholder until this functionality is developed
    status = '~4522'        # placeholder until this functionality is developed
    log = None              # placeholder until this functionality is developed
    # here we run the grs function to get what device to write to
    device_out = str(grs.get_device_out(protocol, step))
    # and now we compile the two items to be returned
    pe_out = [device_out, token, [person, entity, priority, task, task_type, spec, time_posted, time_reposted, status, log]]
    pe_wait = [token, [device_out, log, time_posted, person, entity, caller, protocol, step, thread, flow]]
    return pe_out, pe_wait
# ### END - function to create a pe_out and a pe_wait - called by process_calls and is part of PE ##############


# START - PE - the Protocol Engine #############################################################################
# Effectively "PE" is looking at two different pe_ins lists.
# pe_ins_sol are solicted inputs, have an associated pe_wait in pe_waits, and can carry datas for writing to adat
# pe_ins_unsol are unsolicted inputs, with a different format, no associated pe_wait, and carry no datas for adat
def protocol_engine(pe_ins_sol, pe_waits, pe_ins_unsol, pe_outs):
    global sim_time
    pdata_appendums = []
    adat_appendums = []
    if pe_ins_sol:  # solicited inputs
        pe_in = pe_ins_sol.pop(0)
        pe_wait = pe_waits[pe_in[0]]
        # Here we gather the data to append a new row to pdata
        pdatm = random.randint(100001, 999999)  # this to be replaced by get global next datm call
        person = pe_wait[3]
        entity = pe_wait[4]
        caller = pe_wait[5]
        protocol = pe_wait[6]
        step = pe_wait[7]
        thread = pe_wait[8]
        datas = pe_in[2]
        record_dts = sim_time.get_time_stamp()
        actor = pe_in[2].get('actor')       # why isn't this going somewhere?
        # and then create the row to append and append
        pdata_appendum = [pdatm, person, entity, caller, protocol, step, thread, record_dts, datas]
        pdata_appendums.append(pdata_appendum)
        # Here we gather the addtional data needed to append to adat
        adatm = random.randint(1001, 9999)  # this to be replaced by get global next datm call
        parent = pdatm
        datums = datas['data']
        for datum in datums:
            k = datum['k']
            vt = 'vtvt'   # datum['vt']
            v = datum['v']
            units = 'uu'  # datum['units']
            event_dts = sim_time.get_time_stamp()  # should use simul_clock time for now, someday more complex
            adat_appendum = [person, k, [adatm, entity, parent, vt, v, units, event_dts]]
            adat_appendums.append(adat_appendum)
        # Now we need to process any calls this pe_in made
        calls = pe_wait[9].get('call')
        if calls:
            process_calls(calls, pdata_appendum, pe_outs, pe_waits)
        # And finally need to remove the lines processed from pe_outs and pe_waits
        token = pe_in[0]
        del pe_outs[pe_waits[token][0]][token]
        del pe_waits[token]

    if pe_ins_unsol:  # unsolicited inputs
        # Note: pe_ins_unsol can't can write to adat (only pe_ins_sol can), per concerns if unsol should even be able
        pe_in = pe_ins_unsol.pop(0)
        # Here we compile the data to append a new row to pdata
        pdatm = random.randint(100001, 999999)  # this to be replaced by get global next datm call
        person = pe_in[2].get('person')
        entity = pe_in[2].get('entity')
        caller = None  # since there is no caller row
        protocol = pe_in[0]   # for unsolicited inputs pe_in[0] will be the name of the unsolicited protocol
        step = 1  # hmm - will it always be 1?
        thread = random.randint(100001, 999999)  # this to be replaced by get global next thread call
        datas = None  # Do not expect unsolicted pe_ins to carry data to be written to adat (could be dangerous)
        record_dts = sim_time.get_time_stamp()
        # and then create the row to append and append
        pdata_appendum = [pdatm, person, entity, caller, protocol, step, thread, record_dts, datas]
        pdata_appendums.append(pdata_appendum)
        # Now we need to process any calls this pe_in made
        calls = pe_in[2].get('call')
        if calls:
            process_calls(calls, pdata_appendum, pe_outs, pe_waits)

    return pdata_appendums, adat_appendums

# ## END - PE - the Protocol Engine #############################################################################