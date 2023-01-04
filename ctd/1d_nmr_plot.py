"""
Plot 1D (e.g. 19F) spectra.
"""

import nmrglue as ng
import matplotlib.pyplot as plt
import numpy as np

#plt.style.use("/Users/darian/github/wedap/wedap/styles/default.mplstyle")

def plot_1d(path, ax=None, label=None, color="magenta"):
    """
    Plot 1D NMR spectrum.
    """
    if ax is None:
        fig, ax = plt.subplots()
    else:
        fig = plt.gcf()

    # read in the data from a NMRPipe file
    dic,data = ng.pipe.read(path)

    # create a unit conversion object for the axis
    uc = ng.pipe.make_uc(dic, data)

    # plot the spectrum
    ax.plot(uc.ppm_scale(), data, color=color, label=label)

    # decorate axes
    ax.set_yticklabels([])
    ax.set_yticks([])
    #ax.set_title("CTD $^{19}$F 1D")
    ax.set_xlabel("$^{19}$F ppm")
    ax.set_xlim(-120, -140)
    #ax.set_ylim(-80000, 2500000)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.invert_xaxis()

    # save the figure
    #fig.savefig("spectrum.png") # this can be .pdf, .ps, etc

fig, ax = plt.subplots()

plot_1d("600-2/DTY-CaCTD-F-12152022/1/test.DAT", ax=ax, label="7F", color="k")
plot_1d("600-2/DTY-CaCTD-F-12152022/2/test.DAT", ax=ax, label="4F", color="magenta")

plt.legend(prop={'size': 12})
fig.tight_layout()
plt.show()