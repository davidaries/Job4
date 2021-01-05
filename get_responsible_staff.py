# get_responsible_staff.py
import PEv1_data as PEd


def get_staff_type(protocol, step):  # get the staff_type who is responsible for the step in the protocol
    staffer_type = PEd.protostep_staff[protocol][step]
    return staffer_type


def get_staffer(staff_type):  # get the staffer who is responsible for the step in the protocol
    for s in PEd.staffers:  # currently gets the first staffer who matches on staff_type, much more to be done!
        if PEd.staffers[s]['~23'] == staff_type:
            return s


def get_device_out(protocol, step):
    staff_type = get_staff_type(protocol, step)  # get the responsible staff_type
    staffer = get_staffer(staff_type)  # get the responsible staffer based on staff_type
    device_out = PEd.staff_device[staffer]  # then get the device_out based on the staffer
    return device_out
