"""
Plot 2D EXSY (e.g. 19F-19F) spectra.
"""

import nmrglue as ng
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm

import gif
from tqdm.auto import tqdm

plt.style.use("/Users/darian/github/wedap/wedap/styles/default.mplstyle")

# plot parameters
cmap = matplotlib.cm.Blues_r    # contour map (colors to use for contours)
contour_start = 500000           # contour level start value
contour_num = 8                # number of contour levels
contour_factor = 1.6          # scaling factor between contour levels

# calculate contour levels
cl = contour_start * contour_factor ** np.arange(contour_num) 

def plot_exsy(path, ax=None, color="magenta", title="$^{19}$F-$^{19}$F EXSY"):
    """
    Plot 19F-19F EXSY.

    Parameters
    ----------
    path : str
        Path to nmr data file (e.g. nmrpipe).
    ax : mpl axes object
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
    uc_19fx = ng.pipe.make_uc(dic, data, dim=0)
    ppm_19fx = uc_19fx.ppm_scale()
    ppm_19fx_0, ppm_19fx_1 = uc_19fx.ppm_limits()
    uc_19fy = ng.pipe.make_uc(dic, data, dim=1)
    ppm_19fy = uc_19fy.ppm_scale()
    ppm_19fy_0, ppm_19fy_1 = uc_19fy.ppm_limits()

    # plot the contours (tranpose needed here)
    #ax.contour(data.T, cl, cmap=cmap, extent=(ppm_19fx_0, ppm_19fx_1, ppm_19fy_0, ppm_19fy_1))
    ax.contour(data, cl, colors=color, extent=(ppm_19fx_0, ppm_19fx_1, ppm_19fy_0, ppm_19fy_1), 
               linewidths=1)

    # add grid at each x and y tick
    ax.grid(color='darkgrey', linestyle='-', linewidth=0.5)

    # decorate the axes
    ax.set_ylabel("$^{19}$F (ppm)")
    ax.set_xlabel("$^{19}$F (ppm)")
    ax.set_title(title)
    ax.set_xlim(-126, -125)
    ax.set_ylim(-130, -122)
    ax.invert_xaxis()
    ax.invert_yaxis()


# fig, ax = plt.subplots()
# plot_exsy("600-2/DTY-CaCTD-4F-EXSY-12162022/10/test.DAT", color="magenta", ax=ax)
# fig.tight_layout()
# plt.show()
#fig.savefig("figures/4f_exsy.png", dpi=300, transparent=True)

import matplotlib.cm as cm
from matplotlib.colors import Normalize
import matplotlib

def multi_exsy_plot():
    """
    Plot multiple exsy mixing times with cbar for mixing time.
    TODO
    """
    fig, ax = plt.subplots()
    cmap = cm.viridis
    norm = Normalize(vmin=0, vmax=10)
    for i in range(9, -1, -1):
    #for i in range(2):
        # color needs to be in 1 item list since otherwise, it is rgba multi item tuple
        # this tuple would get interpreted as multiple colors for contours
        color = [cmap(norm(i))]
        plot_exsy(f"600-2/DTY-CaCTD-4F-EXSY-12162022/1{i}/test.DAT", color=color, ax=ax)

    # make cbar axes
    cax, cbar_kwds = matplotlib.colorbar.make_axes(ax, location="top",
                            fraction=1, shrink=0.5, aspect=10, anchor=(1, 1))
    #cax = fig.add_axes([0.95, 0.1, 0.025, 0.4])

    cbar = matplotlib.colorbar.ColorbarBase(cax, cmap=cmap, 
                                        norm=norm,
                                        orientation="horizontal")
    #cbar.add_lines(range(0,vmax + 1), "k", linewidths=1)
    cbar.set_label("Mixing Time (s)", fontweight="bold", labelpad=16)

    fig.tight_layout()
    #plt.tight_layout()
    plt.show()

multi_exsy_plot()

def exsy_gif():
    ### make a gif ###
    # (optional) set the dots per inch resolution to 300:
    #gif.options.matplotlib["dpi"] = 300

    # decorate a plot function with @gif.frame (return not required):
    @gif.frame
    def plot(dir, mixing):
        """
        Make a gif of multiple EXSY plots.

        Parameters
        ----------
        dir : int
        mixing : int
            mixing time OF EXSY experiment.
        """
        dir += 10
        fig, ax = plt.subplots()
        plot_exsy(f"600-2/DTY-CaCTD-4F-EXSY-12162022/{dir}/test.DAT", ax=ax, 
                title="$^{19}$F-$^{19}$F EXSY: Mixing Time = " + str(mixing) + "ms")
        fig.tight_layout()

    # build a bunch of "frames"
    frames = []
    # loop each mixing time
    times = [2, 5, 10, 15, 25, 35, 50, 75, 100, 200, 600]
    for i, mix in enumerate(tqdm(times, desc="GIF Progress")):
        frame = plot(i, mix)
        frames.append(frame)

    # specify the duration between frames (milliseconds) and save to file:
    gif.save(frames, "figures/exsy_lp.gif", duration=500)

#exsy_gif()

def plot_iratios():
    # from looking at peak heights, amplitudes, and nmrpipe peak heights
    # the first peak 2 peaks picked can be used for I ratio
    # I_12 / I_11
    ### plot the intensity ratio over mixing times
    #times = [2, 5, 10, 15, 25, 35, 50, 75, 100, 200, 600]
    times = [2, 5, 10, 15, 25, 35, 50, 75, 100, 200]
    ratios = []
    for i, time in enumerate(times):
        i += 10
        # read in the data from a NMRPipe file
        dic, data = ng.pipe.read(f"600-2/DTY-CaCTD-4F-EXSY-12162022/{i}/test.DAT")
        peaks = ng.peakpick.pick(data, 350000, cluster=False)
        #print(peaks)

        # peak D1 D1
        loc11_x = int(peaks[0][0])
        loc11_y = int(peaks[0][1])

        # peak D1 D2
        loc12_x = int(peaks[1][0])
        loc12_y = int(peaks[1][1])

        # extracting intensity from array
        i11 = data[loc11_x, loc11_y]
        i12 = data[loc12_x, loc12_y]

        # ratio of i12 / i11
        iratio = i12 / i11
        if iratio > 1:
            print(peaks)
        ratios.append(iratio)
        print(iratio)

    # save ratios to file
    np.savetxt("iratios_4F.txt", ratios, delimiter="\t")

    plt.scatter(times, ratios)
    plt.xlim(-10, 210)
    plt.ylim(0, 0.6)
    plt.xlabel("Time (ms)")
    plt.ylabel("I$_{12}$/I$_{11}$")
    #plt.title("")
    plt.tight_layout()
    plt.savefig("figures/Iratios_4F.png", dpi=300, transparent=True)
    plt.show()

#plot_iratios()