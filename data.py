"""data.py is in charge of managing and returning the data used in this program
    :param medium_font: creates a medium sized font used in the GUI
    :type medium_font: Font
    :param larger_font: creates a larger sized font used in the GUI
    :type larger_font: Font
"""
from tkinter import font as tk_font

medium_font = None
larger_font = None


class ListItems:
    """ListItems is a class that stores various lists used by the rest of the program for retrieving information
        :param language_preference: is a value that contains the primary language for the program
        :type language_preference: str
        :param staffers: staffers is a nested list of staff members where each staff member (in staff_members list)
            contains the following variables:
            [name(str), roll(str), language_preference(str)]
        :param staff_device: a list of dictionaries linking a staff member's name to their screen's id
        :type staffers: list
        :param pei_q: a list for storing values given back from the UI after being processed.  Currently not in use
        :type pei_q: list
        :param peo_q: a nested list that contains queue information to be polled by the staffer based on their device id
        :type peo_q: list
        :param choices: values for drop down menus and check boxes for use in the UI
        :type choices: list
        :param pdata: a nested list that contains the information about the people being processed
        :type pdata: list
    """
    # staff_device = [{staff_name: device_numer}, …]
    staff_device = [{'Joe': 123}, {'Jose': 234}, {'Maria': 345}, {'Mary': 456}]
    # staffers to replace staffers above -- 2nd item in the list is their role.
    staffers = [['Joe', '~24', '~101'], ['Jose', '~25', '~102'], ['Maria', '~26', '~101'], ['Mary', '~27', '~102']]

    pei_q = []

    # peo_q = [device_out[0], token[1], person[2], priority[3], time_posted[4], time_reposted[5], status[6],
    #                log[7], time_complete[8], device_in[9], protocol[10], step[11], task[12], tasktype[13], spec[14]]
    peo_q = [
        [123, 2222, 11, 1, 1604712242.31, None, 'n', None, None, None, 1, 1, '~34', 'UI',
         [['PersonHeader'], ['ModifyEntry', '~16'], ['Button', '~20']]],
        [234, 2223, 11, 2, 1604712242.32, None, 'n', None, None, None, 1, 2, '~35', 'UI',
         [['PersonHeader'], ['TaskHeader'],
          ['EmptyEntry', '~19'], ['DropDown', '~17', 'c117'], ['Button', '~20']]],
        [345, 2224, 11, 3, 1604712242.33, None, 'n', None, None, None, 1, 3, '~36', 'UI',
         [['PersonHeader'], ['TaskHeader'],
          ['Fixed', '~17'], ['DropDown', '~2', 'c102'], ['Button', '~20']]],
        [456, 2225, 11, 4, 1604712242.34, None, 'n', None, None, None, 1, 4, '~18', 'UI',
         [['PersonHeader'], ['TaskHeader'],
          ['Fixed', '~2'], ['CheckBoxes', '~18', 'c118'], ['Button', '~20']]],
        [123, 3333, 12, 1, 1604712242.35, None, 'n', None, None, None, 1, 1, '~34', 'UI',
         [['PersonHeader'], ['ModifyEntry', '~16'], ['Button', '~20']]],
        [234, 3334, 12, 2, 1604712242.36, None, 'n', None, None, None, 1, 2, '~35', 'UI',
         [['PersonHeader'], ['TaskHeader'],
          ['EmptyEntry', '~19'], ['DropDown', '~17', 'c117'], ['Button', '~20']]],
        [345, 3335, 12, 3, 1604712242.37, None, 'n', None, None, None, 1, 3, '~36', 'UI',
         [['PersonHeader'], ['TaskHeader'],
          ['Fixed', '~17'], ['DropDown', '~2', 'c102'], ['Button', '~20']]],
        [456, 3336, 12, 4, 1604712242.38, None, 'n', None, None, None, 1, 4, '~18', 'UI',
         [['PersonHeader'], ['TaskHeader'],
          ['Fixed', '~2'], ['CheckBoxes', '~18', 'c118'], ['Button', '~20']]]
    ]

    # Also, to populate dropboxes or checkboxes, let’s use this format.
    # See PEO-Q spec v2b.xlsx cell S5 for explanation of this.
    choices = {
        'c117': [['~28', True], ['~29', True]],
        'c102': [['~5', True], ['~30', True]],
        'c118': [['~31', True], ['~32', True]],
    }

    language_preference = ('~101')

    # Offset
    #      0   1  2    3    4  5     6     7     8    9    10  11      12   .....
    pdata = [
        (101, 1, 11, None, 1, None, None, None, 101, '~1', 4, 'Tina', None, None, None, None, None, 1603824276.5, None,
         None, None, None, None, None),
        (102, 1, 11, None, 1, None, None, None, 101, '~14', 0, '~22', None, None, None, None, None, 1603824276.5,
         None, None, None, None, None, None),
        (103, 1, 11, None, 1, None, None, None, 101, '~15', 1, 40, None, None, None, None, None, 1603824276.5, None,
         None, None, None, None, None),
        (104, 1, 11, None, 1, None, None, None, 101, '~16', 4, '202-5431', None, None, None, None, None, 1603824276.5,
         None, None, None, None, None, None),
        (105, 1, 12, None, 2, None, None, None, 102, '~1', 4, 'Tony', None, None, None, None, None, 1603824276.5, None,
         None, None, None, None, None),
        (106, 1, 12, None, 2, None, None, None, 102, '~14', 0, '~21', None, None, None, None, None, 1603824276.5, None,
         None, None, None, None, None),
        (107, 1, 12, None, 2, None, None, None, 102, '~15', 1, 35, None, None, None, None, None, 1603824276.5, None,
         None, None, None, None, None),
        (108, 1, 12, None, 2, None, None, None, 102, '~16', 4, '703-3341', None, None, None, None, None, 1603824276.5,
         None, None, None, None, None, None),
        (109, 1, 11, None, 1, None, None, None, 101, '~17', 4, '~28', None, None, None, None, None, 1603824276.5, None,
         None, None, None, None, None),
        (110, 1, 11, None, 1, None, None, None, 101, '~2', 4, '~5', None, None, None, None, None, 1603824276.5, None,
         None, None, None, None, None),
        (111, 1, 12, None, 2, None, None, None, 102, '~17', 4, '~29', None, None, None, None, None, 1603824276.5, None,
         None, None, None, None, None),
        (112, 1, 12, None, 2, None, None, None, 102, '~2', 4, '~30', None, None, None, None, None, 1603824276.5, None,
         None, None, None, None, None)
        ]


Lists = ListItems()


def get_data(listname, offset1=None, criteria1=None, offset2=None, criteria2=None):
    """returns from the Class Lists the list named listname, optionally filtered using up to two fields and
       criteria for those field(s).

    :param listname: name of the list to return
    :type listname: str
    :param offset1: offset of the first field to use as filter a filter
    :type offset1: int
    :param criteria1: criteria to match for in the first field
    :type criteria1: int or str
    :param offset2: offset of the second field to use as filter a filter
    :type offset2: int
    :param criteria2: criteria to match for in the second field
    :type criteria2: int or str
    :return: list listname as optionally filtered
    :rtype: list
    """
    if offset1 is None:
        return getattr(Lists, listname)
    elif offset2 is None:
        li = getattr(Lists, listname)
        return [li for li in li if li[offset1] == criteria1]
    else:
        li = getattr(Lists, listname)
        return [li for li in li if (li[offset1] == criteria1 and li[offset2] == criteria2)]


def create_fonts(master):
    """This function generates and stores the fonts to be used in the program so they do not need to be created
        multiple times throughout the program
        :param master: takes in the reference to the main program window, which is needed to create the following fonts
        :type master: tkinter class window reference
        """
    global medium_font, larger_font
    root = master
    medium_font = tk_font.Font(root=root.master, family='Helvetica', size=10, weight=tk_font.BOLD)
    larger_font = tk_font.Font(root=root.master, family='Helvetica', size=12, weight=tk_font.BOLD)

def get_large_font():
    """method to return the larger font to be used in other classes
        :returns: the layout for the larger font size
        :rtype: Font """
    return larger_font


def get_medium_font():
    """method to return the medium font to be used in other classes
        :returns: the layout for the medium font size
        :rtype: Font """
    return medium_font
