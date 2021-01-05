"""PEv1_data.py is in charge of managing and returning the data used in this program

"""
# COMPARE THIS WITH STAFFERS: should PersonHeader, TaskHeader, etc be ~vocab?

# We should be loading from a protocol table, which has these fields
# protocol, step, step_type, description, task, task_type, spec, write, flow
# And creates a protocol dictionary, which has entries like follows:
# step_type[0], task[1], task_type[2], spec[3], write[4], flow[5]

p0001 = {         # not clear to me we need tuples within a tuple like this
    1: ['st_1', '~34', 'UI', ('PersonHeader', 'TaskHeader',
        ('ModifyEntry', '~16'), ('Button', '~20')), None, ({'call': [['p0001', 2, 3]]})],
    2: ['st_1', '~35', 'UI', ('PersonHeader', 'TaskHeader',
        ('EmptyEntry', '~19'), ('DropDown', '~17', 'c117'), ('Button', '~20')), None, ({'call': [['p0001', 3, 3]]})],
    3: ['st_1', '~36', 'UI', ('PersonHeader', 'TaskHeader',
        ('Fixed', '~17'), ('DropDown', '~2', 'c102'), ('Button', '~20')), None, ({'call': [['p0001', 4, 3]]})],
    4: ['st_1', '~18', 'UI', ('PersonHeader', 'TaskHeader',
        ('Fixed', '~2'), ('CheckBoxes', '~18', 'c118'), ('Button', '~20')), None, ({})]
}

ip01 = {
    1: ['st_1', '~ip01_task', '~ip01_task_type', None, None, ({'call': [['p0001', 1, 3]]})]
}

protocols = {
    'p0001': p0001,
    'ip01': ip01,
}

p0001_staff = {
    1: '~24', 2: '~25', 3: '~26', 4: '~27'
}
protostep_staff = {
    'p0001': p0001_staff
}

# For each choice: True means it goes in the short list, False means it is only in the complete list.
# e.g. for c102, ~5 and ~30 show in the short list
# then, there should be some kind of divider (even just a '----------------')
# and then the complete list of all five: ~5, ~30, ~37, ~38, ~39
# with both the short and the complete list alphabetized based on the staff's language preference
choices = {
    'c117': [['~28', True], ['~29', True]],
    'c102': [['~5', True], ['~30', True], ['~37', False], ['~38', False], ['~39', False]],
    'c118': [['~31', True], ['~32', True]],
     }


staffers = {
            's001': {'~1': 'Joe', '~23': '~24', '~100': '~101'},
            's002': {'~1': 'Jose', '~23': '~25', '~100': '~102'},
            's003': {'~1': 'Maria', '~23': '~26', '~100': '~101'},
            's004': {'~1': 'Mary', '~23': '~27', '~100': '~102'}
            }


staff_device = {'s001': '123', 's002': '234', 's003': '345', 's004': '456'}
device_staff = {'123': 's001', '234': 's002', '345': 's003', '456': 's004'}

