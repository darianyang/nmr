"""
Code to plot peak labels (e.g. on an HSQC).
"""

import numpy as np
import matplotlib.pyplot as plt

def proc_ctd_shifts(shift_file):
    """
    CA CTD shifts are in BMRB assignment style.
    Returns new array: x = residue number, y1 = atom type, y2 = shift value (ppm).
    TODO: this could be much more efficient as vector operations.
    """
    # split res num column by '.' to extract res num
    x = [int((x.split('.'))[0]) for x in open(shift_file).readlines()]
    # get rid of first 4 char (res num) and keep atom type
    y1 = [str((y1.split())[0])[4:] for y1 in open(shift_file).readlines()]
    # split by space (default) and extract shift float value
    y2 = [float((y2.split())[1]) for y2 in open(shift_file).readlines()]

    # return 3 column array / 3 item list of lists
    ctd_shifts = []
    ctd_shifts.append(x)
    ctd_shifts.append(y1)
    ctd_shifts.append(y2)

    # from 3 rowsx and n cols to 3 cols and n rows
    ctd_shifts = np.array(ctd_shifts).T

    return ctd_shifts

#shifts = proc_ctd_shifts("ctd/CA_CTD_BMRB_assignments.shifts")
#print(np.unique(shifts[:,0]).shape)
#print(shifts[shifts[:,0] == "146"])

def peak_text_plotter(shifts, color="k", ax=None, redlist=None):
    """
    Plot the 1H-15N peaks from peak_list array.
    shifts = 3 cols: resnum | atom_name | shift_val

    Parameters
    ----------
    shifts : str or array
        Can be file path or prefomatted array.
    color : str
    ax : mpl axes object
    redlist : list
        List of residue number to mark in red.
    """
    # if file path, gen list of shifts
    if isinstance(shifts, str):
        shifts = proc_ctd_shifts(shifts)

    # allow custom axes objects
    if ax is None:
        fig, ax = plt.subplots()
    else:
        fig = plt.gcf()

    # unique residue ids
    resids = np.unique(shifts[:,0])
    
    # reformat array to N and NH pairs (resid | X/H shift | Y/N shift)
    peaks = np.zeros((resids.shape[0], 3))
    # add resids to first col
    peaks[:,0] = resids

    # loop unique residue numbers
    for i, res in enumerate(resids):
        # look into the overall peaklist for res shifts
        for shift in shifts[shifts[:,0] == res]:
            # if the atom name is correct, add to shifts array
            if shift[1] == "HN":
                # assign column X shift value
                peaks[i, 1] = shift[2]
            if shift[1] == "N":
                # assign column Y shift value
                peaks[i, 2] = shift[2]

    # filter peaks with no H/NH assignments (e.g. PRO)
    peaks = peaks[peaks[:,1] != 0]

    # plot peak assignments
    for peak in peaks:
        if redlist is not None and int(peak[0]) in redlist:
            plt.text(peak[1], peak[2], int(peak[0]), fontsize=8, 
                     color="red", ha="center", va="center")
        else:
            plt.text(peak[1], peak[2], int(peak[0]), fontsize=8, 
                     color=color, ha="center", va="center")


# shifts = proc_ctd_shifts("ctd/CA_CTD_BMRB_assignments.shifts")
# peak_text_plotter(shifts)

# peak_text_plotter("ctd/CA_CTD_BMRB_assignments.shifts")
# plt.xlim(5,9)
# plt.ylim(110,130)
# plt.show()