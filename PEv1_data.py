"""PEv1_data.py is data to be used in this program
   In the future such data will be loaded from tables, not come from this module.

"""

# We will be loading from a protocol table, which has these fields
# protocol, step, step_type, description, task, task_type, spec, write, flow
# And and were creating protocol dictionary, which has these fields:
# step_type[0], task[1], task_type[2], spec[3], write[4], flow[5]

p0001 = {      # this is what protocol p0001 with its four steps will look like when loaded from the table
    1: ['st_1', '~34', 'UI', ('PersonHeader', 'TaskHeader',
        ('ModifyEntry', '~16'), ('Button', '~20')), None, ({'call': [['p0001', 2, 3]]})],
    2: ['st_1', '~35', 'UI', ('PersonHeader', 'TaskHeader',
        ('EmptyEntry', '~19'), ('DropDown', '~17', 'c117'), ('Button', '~20')), None, ({'call': [['p0001', 3, 3]]})],
    3: ['st_1', '~36', 'UI', ('PersonHeader', 'TaskHeader',
        ('Fixed', '~17'), ('DropDown', '~2', 'c102'), ('Button', '~20')), None, ({'call': [['p0001', 4, 3]]})],
    4: ['st_1', '~18', 'UI', ('PersonHeader', 'TaskHeader',
        ('Fixed', '~2'), ('CheckBoxes', '~18', 'c118'), ('Button', '~20')), None, ({})]
}

ip01 = {       # this is what the intake protocol ip-1 with its one step will look like when loaded from the table
    1: ['st_1', '~ip01_task', '~ip01_task_type', None, None, ({'call': [['p0001', 1, 3]]})]
}

protocols = {      # here we create the protocols dictionary and load the two protocols into it.
    'p0001': p0001,
    'ip01': ip01,
}

p0001_staff = {     # assigning a staff type to each step in protocol p0001
    1: '~24', 2: '~25', 3: '~26', 4: '~27'
}
protostep_staff = {     # putting the staff type assignments for protocol p0001 into the protostep_staff  dictionary
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


staffers = {                # a primitive dictionary for staffers that will do for now
            's001': {'~1': 'Joe', '~23': '~24', '~100': '~101'},
            's002': {'~1': 'Jose', '~23': '~25', '~100': '~102'},
            's003': {'~1': 'Maria', '~23': '~26', '~100': '~101'},
            's004': {'~1': 'Mary', '~23': '~27', '~100': '~102'}
            }

# these next two rows to be dynamically generated when we have staff login in place.
staff_device = {'s001': 123, 's002': 234, 's003': 345, 's004': 456}
device_staff = {123: 's001', 234: 's002', 345: 's003', 456: 's004'}

staffer_login_info = {'s001': ['pass', False], 's002': ['pass', False], 's003': ['pass', False], 's004': ['pass', False]}

entrants = [['7:05', 'pers101'],  ['7:10', 'pers102'],  ['7:15', 'pers103'],  ['7:20', 'pers104'],  ['7:25', 'pers105']]
# this to replace the pdata section in data.py
# because the UI now queries adat rather than pdata for the values it needs
# adat is a dictionary where the key is the person, and then each person is a dictionary where the key is k, and value is a list with lists (inner lists) within.
# each of the inner lists has the following seven fields.
# adatm[0], entity[1], parent[2], vt[3], v[4], units[5], event_dts[6]
adat = {
    'pers101': {
        '~1': [[101, None, None, 4, 'Tina', None, 1603824276.5]],
        '~14': [[102, None, None, 0, '~22', None, 1603824276.5]],
        '~15': [[103, None, None, 1, 40, '~40', 1603824276.5]],
        '~16': [[104, None, None, 4, '202-888-5431', None, 1603824276.5]],
        '~17': [[105, None, None, 4, '~28', None, 1603824276.5]],
        '~2': [[116, None, None, 4, '~5', None, 1603824276.5]],
        '~19': [[113, None, None, 1, 50, '~41', 1603800000.5],
                [114, None, None, 1, 51, '~41', 1603812000.5],
                [115, None, None, 1, 52, '~41', 1603824276.5]]
    },
    'pers102': {
        '~1': [[107, None, None, 4, 'Tony', None, 1603824276.5]],
        '~14': [[108, None, None, 0, '~21', None, 1603824276.5]],
        '~15': [[109, None, None, 1, 35, '~40', 1603824276.5]],
        '~16': [[110, None, None, 4, '703-999-3341', None, 1603824276.5]],
        '~17': [[111, None, None, 4, '~29', None, 1603824276.5]],
        '~2': [[112, None, None, 4, '~30', None, 1603824276.5]],
        '~19': [[116, None, None, 1, 75, '~41', 1603800000.5],
                [117, None, None, 1, 74, '~41', 1603812000.5],
                [118, None, None, 1, 75, '~41', 1603824276.5]]
    },
    'pers103': {
        '~1': [[121, None, None, 4, 'Bill', None, 1603824276.5]],
        '~14': [[122, None, None, 0, '~21', None, 1603824276.5]],
        '~15': [[123, None, None, 1, 21, '~40', 1603824276.5]],
        '~16': [[124, None, None, 4, '703-999-8888', None, 1603824276.5]],
        '~17': [[125, None, None, 4, '~29', None, 1603824276.5]],
        '~2': [[126, None, None, 4, '~30', None, 1603824276.5]],
        '~19': [[127, None, None, 1, 88, '~41', 1603800000.5],
                [128, None, None, 1, 92, '~41', 1603812000.5],
                [129, None, None, 1, 94, '~41', 1603824276.5]]
    },
    'pers104': {
        '~1': [[131, None, None, 4, 'Mary', None, 1603824276.5]],
        '~14': [[132, None, None, 0, '~22', None, 1603824276.5]],
        '~15': [[133, None, None, 1, 66, '~40', 1603824276.5]],
        '~16': [[134, None, None, 4, '703-999-1111', None, 1603824276.5]],
        '~17': [[135, None, None, 4, '~29', None, 1603824276.5]],
        '~2': [[136, None, None, 4, '~30', None, 1603824276.5]],
        '~19': [[137, None, None, 1, 44, '~41', 1603800000.5],
                [138, None, None, 1, 43, '~41', 1603812000.5],
                [139, None, None, 1, 42, '~41', 1603824276.5]]
    },
    'pers105': {
        '~1': [[141, None, None, 4, 'Lisa', None, 1603824276.5]],
        '~14': [[142, None, None, 0, '~22', None, 1603824276.5]],
        '~15': [[143, None, None, 1, 35, '~40', 1603824276.5]],
        '~16': [[144, None, None, 4, '703-999-3341', None, 1603824276.5]],
        '~17': [[145, None, None, 4, '~29', None, 1603824276.5]],
        '~2': [[146, None, None, 4, '~30', None, 1603824276.5]],
        '~19': [[147, None, None, 1, 54, '~41', 1603800000.5],
                [148, None, None, 1, 56, '~41', 1603812000.5],
                [149, None, None, 1, 53, '~41', 1603824276.5]]
    }
}