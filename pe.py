# pe.py

import datetime
import random
import PEv1_data as PEd
import get_responsible_staff as grs


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
    # for reference pdata_appendum = [pdatm[0], meta_pdatm[1], person[2], entity[3], caller[4], protocol[5], step[6], thread[7], record_dts[8], datas_write[9], actor[10]]
    protocol, step, priority = protostep[0], protostep[1], protostep[2]
    token = random.randint(1000000000000001, 9999999999999999)   # the token is used later to match a pe_in (from the UI) with its corresponding pe_wait
    # the next fields are read directly from pdata_addendum
    caller = pdata_appendum[0]
    meta_pdatm = pdata_appendum[1]
    person = pdata_appendum[2]
    entity = pdata_appendum[3]
    thread = pdata_appendum[7]
    if step == 1:   # if this is the first step in a protocol it needs a new thread number
        thread = random.randint(100001, 999999)
    # the next four are from the protocol specification for that step
    task = PEd.protocols[protocol][step][1]
    task_type = PEd.protocols[protocol][step][2]
    spec = PEd.protocols[protocol][step][3]
    flow = PEd.protocols[protocol][step][5]
    # then a few more loose fields
    time_posted = datetime.datetime.now().timestamp()
    time_reposted = None    # placeholder until this functionality is developed
    status = '~4522'        # placeholder until this functionality is developed
    log = None              # placeholder until this functionality is developed
    # here we run the grs function to get what device to write to
    device_out = str(grs.get_device_out(protocol, step))
    # and now we compile the two items to be returned
    pe_out = [device_out, token, [person, entity, priority, task, task_type, spec, time_posted, time_reposted, status, log]]
    pe_wait = [token, [device_out, log, time_posted, meta_pdatm, person, entity, caller, protocol, step, thread, flow]]
    return pe_out, pe_wait
# ### END - function to create a pe_out and a pe_wait - called by process_calls and is part of PE ##############


# START - PE - the Protocol Engine #############################################################################
# Effectively "PE" is looking at two different pe_ins lists.
# pe_ins_sol are solicted inputs, have an associated pe_wait in pe_waits, and can carry datas for writing to adat
# pe_ins_unsol are unsolicted inputs, with a different format, no associated pe_wait, and carry no datas for adat
def protocol_engine(pe_ins_sol, pe_waits, pe_ins_unsol, pe_outs):
    pdata_appendums = []
    if pe_ins_sol:  # solicited inputs
        pe_in = pe_ins_sol.pop(0)
        pe_wait = pe_waits[pe_in[0]]
        # Here we gather the data to append a new row to pdata
        pdatm = random.randint(100001, 999999)  # this to be replaced by get global next datm call
        meta_pdatm = None  # for now
        person = pe_wait[4]
        entity = pe_wait[5]
        caller = pe_wait[6]
        protocol = pe_wait[7]
        step = pe_wait[8]
        thread = pe_wait[9]
        datas = pe_in[2]
        datas_write = datas  # need a function here use datas and the protocol write field to specify what to write
        record_dts = datetime.datetime.now().timestamp()
        actor = pe_in[2].get('actor')
        # and then create the row to append and append
        pdata_appendum = [pdatm, meta_pdatm, person, entity, caller, protocol, step, thread, record_dts, datas_write, actor]
        pdata_appendums.append(pdata_appendum)
        # Now we need to process any calls this pe_in made
        calls = pe_wait[10].get('call')
        if calls:
            process_calls(calls, pdata_appendum, pe_outs, pe_waits)
        # And finally need to remove the lines processed from pe_outs and pe_waits
        token = pe_in[0]
        del pe_outs[pe_waits[token][0]][token]
        del pe_waits[token]

    if pe_ins_unsol:  # unsolicited inputs
        pe_in = pe_ins_unsol.pop(0)
        # Here we compile the data to append a new row to pdata
        pdatm = random.randint(100001, 999999)  # this to be replaced by get global next datm call
        meta_pdatm = None  # for now
        person = pe_in[2].get('person')
        entity = pe_in[2].get('entity')
        caller = None  # since there is no caller row
        protocol = pe_in[0]   # for unsolicited inputs pe_in[0] will be the name of the unsolicited protocol
        step = 1  # hmm - will it always be 1?
        thread = random.randint(100001, 999999)  # this to be replaced by get global next thread call
        datas_write = None  # Do not expect unsolicted pe_ins to carry data to be written to adat (could be dangerous)
        record_dts = datetime.datetime.now().timestamp()
        actor = pe_in[2].get('actor')
        # and then create the row to append and append
        pdata_appendum = [pdatm, meta_pdatm, person, entity, caller, protocol, step, thread, record_dts, datas_write, actor]
        pdata_appendums.append(pdata_appendum)
        # Now we need to process any calls this pe_in made
        calls = pe_in[2].get('call')
        if calls:
            process_calls(calls, pdata_appendum, pe_outs, pe_waits)

    return pdata_appendums

# ## END - PE - the Protocol Engine #############################################################################
