"""
Plot 2D HSQC (e.g. 1H-15N) spectra.
"""

import nmrglue as ng
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm

import plot_peak_labels

plt.style.use("/Users/darian/github/wedap/wedap/styles/default.mplstyle")

# plot parameters
cmap = matplotlib.cm.Blues_r    # contour map (colors to use for contours)
contour_start = 1500000           # contour level start value
contour_num = 8                # number of contour levels
contour_factor = 1.8          # scaling factor between contour levels

# calculate contour levels
cl = contour_start * contour_factor ** np.arange(contour_num) 

def plot_hsqc(path, ax=None, label=None, color="magenta", title="CTD HSQC"):
    """
    Plot 1H-15N HSQC.

    Parameters
    ----------
    path : str
        Path to nmr data file (e.g. nmrpipe).
    ax : mpl axes object
    label : str
        Plot label
    color : str
        Plot color
    title : str
        Plot title
    """
    if ax is None:
        fig, ax = plt.subplots()
    else:
        fig = plt.gcf()

    # read in the data from a NMRPipe file
    dic, data = ng.pipe.read(path)

    # make ppm scales
    uc_1h = ng.pipe.make_uc(dic, data, dim=0)
    ppm_1h = uc_1h.ppm_scale()
    ppm_1h_0, ppm_1h_1 = uc_1h.ppm_limits()
    uc_15n = ng.pipe.make_uc(dic, data, dim=1)
    ppm_15n = uc_15n.ppm_scale()
    ppm_15n_0, ppm_15n_1 = uc_15n.ppm_limits()

    # plot the contours (tranpose needed here)
    #ax.contour(data.T, cl, cmap=cmap, extent=(ppm_1h_0, ppm_1h_1, ppm_15n_0, ppm_15n_1))
    ax.contour(data.T, cl, colors=color, extent=(ppm_1h_0, ppm_1h_1, ppm_15n_0, ppm_15n_1), 
               linewidths=0.25, label=label)

    # add grid at each x and y tick
    ax.grid(color='darkgrey', linestyle='-', linewidth=0.5)

    # decorate the axes
    ax.set_ylabel("$^{15}$N (ppm)")
    ax.set_xlabel("$^{1}$H (ppm)")
    ax.set_title(title)
    ax.set_xlim(6, 11)
    ax.set_ylim(100, 135)
    ax.invert_xaxis()
    ax.invert_yaxis()


fig, ax = plt.subplots()

plot_hsqc("800/DTY-CaCTD-15NFW-12162022/1/test.DAT", color="k", ax=ax)
plot_hsqc("800/DTY-CaCTD-15NFW-12162022/3/test.DAT", color="magenta", ax=ax)

# peak label plotting function
plot_peak_labels.peak_text_plotter("CA_CTD_BMRB_assignments.shifts", ax=ax)

ax.set_title("CTD WT vs 4F")
fig.tight_layout()
plt.show()
#fig.savefig("figures/wt_vs_7f_hsqc.png", dpi=300, transparent=True)