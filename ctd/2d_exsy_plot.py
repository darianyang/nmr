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
#plt.style.use("/Users/darian/github/wedap/styles/poster.mplstyle")

# 4F or 7F
f_pos = "4F"
if f_pos == "4F":
    f_path = "600-2/DTY-CaCTD-4F-EXSY-12162022"
elif f_pos == "7F":
    f_path = "600-2/DTY-CaCTD-7F-EXSY-20Jan2023"

# plot parameters
cmap = matplotlib.cm.Blues_r    # contour map (colors to use for contours)
# # 4F ideal
contour_start = 500000           # contour level start value
contour_num = 8                # number of contour levels
contour_factor = 1.5          # scaling factor between contour levels
# 7F ideal
# contour_start = 1200000           # contour level start value
# contour_num = 8                # number of contour levels
# contour_factor = 1.5          # scaling factor between contour levels

# calculate contour levels
cl = contour_start * contour_factor ** np.arange(contour_num) 

def plot_exsy(path, ax=None, color="magenta", title=None):
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

    # plot the contours (tranpose needed here?)
    # TODO: change extent to make x and y axes consistent?
    #ax.contour(data.T, cl, cmap=cmap, extent=(ppm_19fx_0, ppm_19fx_1, ppm_19fy_0, ppm_19fy_1))
    ax.contour(data, cl, colors=color, extent=(ppm_19fx_0, ppm_19fx_1, ppm_19fy_0, ppm_19fy_1), 
               linewidths=1)
    #ax.contour(data, cl, colors=color, linewidths=1)

    # add grid at each x and y tick
    ax.grid(color='darkgrey', linestyle='-', linewidth=0.5)

    # decorate the axes
    # ax.set_ylabel("$^{19}$F (ppm)")
    # ax.set_xlabel("$^{19}$F (ppm)")
    ax.set_title(title)
    # ax.set_xlim(-126, -125.2)
    # ax.set_ylim(-131, -122)
    ax.set_xlim(-125.9, -125.3)
    #ax.set_ylim(-129.5, -123)
    ax.set_ylim(-130.5, -123)
    ax.invert_xaxis()
    ax.invert_yaxis()


# fig, ax = plt.subplots()
# plot_exsy(f"{f_path}/2/test.DAT", color="magenta", ax=ax)
# fig.tight_layout()
# plt.show()
#fig.savefig(f"figures/{f_pos}_exsy.png", dpi=300, transparent=True)

import matplotlib.cm as cm
from matplotlib.colors import Normalize
import matplotlib

def multi_exsy_plot(path):
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
        plot_exsy(f"{f_path}/1{i}/test.DAT", color=color, ax=ax)

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

#multi_exsy_plot()

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
        if f_pos == "4F":
            dir += 10
        elif f_pos == "7F":
            dir += 1
        fig, ax = plt.subplots()
        plot_exsy(f"{f_path}/{dir}/test.DAT", ax=ax, 
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
    gif.save(frames, f"figures/{f_pos}_exsy.gif", duration=500)

#exsy_gif()

def four_panel_exsy():
    times = [2, 5, 10, 15, 25, 35, 50, 75, 100, 200, 600]
    # if f_pos == "4F":
    #     dir += 10
    # elif f_pos == "7F":
    #     dir += 1

    # fig, ax = plt.subplots()
    # plot_exsy(f"{f_path}/11/test.DAT", ax=ax, 
    #         title="Mixing Time = " + str(times[0]) + "ms")

    fig, ax = plt.subplots(ncols=2, nrows=2, sharex=False, sharey=False, figsize=(6,4))
    #xticks = [-125.4, -125.8]
    xticks = [-125.48, -125.725]
    #yticks = [-123, -126, -129]
    yticks = [-125.08, -127.53]
    # 2 5 50 200
    for i, mt in enumerate([0, 1, 6, 9]):
        plot_exsy(f"{f_path}/1{mt}/test.DAT", ax=ax.flatten()[i]) 
             #title=str(times[mt]) + "ms")  
        ax.flatten()[i].set_xticks(xticks)
        ax.flatten()[i].set_yticks(yticks)
    # plot_exsy(f"{f_path}/10/test.DAT", ax=ax.flatten()[0])
    # plot_exsy(f"{f_path}/11/test.DAT", ax=ax.flatten()[1])
    # plot_exsy(f"{f_path}/16/test.DAT", ax=ax.flatten()[2])
    # plot_exsy(f"{f_path}/19/test.DAT", ax=ax.flatten()[3]) 

    # fig.supxlabel("$^{19}$F (ppm)", fontweight="bold")
    # fig.supylabel("$^{19}$F (ppm)", fontweight="bold")

    fig.text(0.55, 0.015, "$^{19}$F (ppm)", ha='center', fontweight="bold", fontsize=17)
    fig.text(0.001, 0.5, "$^{19}$F (ppm)", va='center', rotation='vertical', fontweight="bold", fontsize=17)

    # t(m) labels
    fig.text(0.25, 0.85, "2 ms",  va='center', ha='center', fontsize=15)
    fig.text(0.635, 0.85, "5 ms",  va='center', ha='center', fontsize=15)
    fig.text(0.25, 0.48, "50 ms",  va='center', ha='center', fontsize=15)
    fig.text(0.645, 0.48, "200 ms",  va='center', ha='center', fontsize=15)

    # get rid of white space
    # plot 1
    ax[0,0].set_xticklabels([])
    ax[0,0].set_yticklabels([-47.5, -48.6], fontsize=14)
    # plot 2
    ax[0,1].set_xticklabels([])
    ax[0,1].set_yticklabels([])
    # plot 3
    ax[1,0].set_xticklabels([-47.5, -48.6], fontsize=14)
    ax[1,0].set_yticklabels([-47.5, -48.6], fontsize=14)
    # plot 4
    ax[1,1].set_xticklabels([-47.5, -48.6], fontsize=14)
    ax[1,1].set_yticklabels([])
    plt.subplots_adjust(hspace=0, wspace=0)
    fig.tight_layout(pad=2.5, h_pad=0, w_pad=0)

    #plt.savefig("figures/4panel.png", dpi=600, transparent=True)
    #plt.savefig("figures/4panel-5.png", dpi=600, transparent=True)
    #plt.savefig("figures/4panel-nogrid.pdf")
    plt.show()

four_panel_exsy()

def plot_iratios():
    # from looking at peak heights, amplitudes, and nmrpipe peak heights
    # the first peak 2 peaks picked can be used for I ratio
    # I_12 / I_11
    ### plot the intensity ratio over mixing times
    #times = [2, 5, 10, 15, 25, 35, 50, 75, 100, 200, 600]
    times = [2, 5, 10, 15, 25, 35, 50, 75, 100, 200]
    #times = [2, 5, 10]
    ratios = []
    errors = []
    for i, time in enumerate(times):
        if f_pos == "4F":
            i += 10
            cut = 450000
            lim = 0.6
            #center = 297
            center = 297
            # TODO: need to plot on spectrum to confirm peak position
            loc_11 = (224, 1940)
            loc_12 = (224, 2426)
        elif f_pos == "7F":
            i += 1
            cut = 1500000
            lim = 0.2
            center = 279
            # TODO: need to plot on spectrum to confirm peak position
            loc_11 = (188, 1810)
            loc_12 = (188, 2401)
        # read in the data from a NMRPipe file
        # shape (512, 4096)
        dic, data = ng.pipe.read(f"{f_path}/{i}/test.DAT")
        #print(data.shape)
        peaks = ng.peakpick.pick(data, cut, cluster=False)
        #print(peaks)

        # peak D1 D1
        # loc11_x = int(peaks[0][0])
        # loc11_y = int(peaks[0][1])
        # # peak D1 D2
        # loc12_x = int(peaks[1][0])
        # loc12_y = int(peaks[1][1])

        # extracting intensity from array
        # i11 = data[loc11_x, loc11_y]
        # i12 = data[loc12_x, loc12_y]
        i11 = data[loc_11[0], loc_11[1]]
        i12 = data[loc_12[0], loc_12[1]]

        # diagonal auto peak (TODO)
        #diag2_x = int(peaks[diag_pos][0])

        # uncertainty from random noise in peak ratio
        # using the central row intensities should work well (no signals)
        #noise = data[int(((loc11_x + diag2_x) / 2)),:]
        #noise = data[center, :]
        # or maybe the bottom row?
        noise = data[-1,:]
        #print(noise)
        #print(noise.shape)
        # rmsd of the noise for a non-signal region
        # sqrt(1/n * (x_1^2 + x_2^2 + ... + x_n^2))
        rmsnoise = np.sqrt(np.sum(noise**2) / noise.shape[0])

        # snr = peak_height / rms noise
        snr_11 = i11 / rmsnoise
        #snr_12 = i12 / rmsnoise
        #print(snr_11)

        # intensity ratio of i12 / i11
        iratio = i12 / i11

        # abs uncertainty from random noise in ratio of peak heights (∆R)
        # |ΔR| = 1/SNR_B + R/SNR_B where R = A/B
        dR = (1/snr_11) + (iratio/snr_11)
        errors.append(dR)
        #print(dR/iratio)

        # sometimes the peaks aren't correctly picked (TODO)
        if iratio > 1 or dR > 0.1:
            print(peaks)
        ratios.append(iratio)
        #print(iratio)

    # make array with intensity ratios and errors
    ratios = np.vstack((np.array(ratios), np.array(errors))).T
    #print(ratios)
    #import sys; sys.exit(0)
    # save ratios to file
    np.savetxt(f"iratios_{f_pos}.txt", ratios, delimiter="\t")

    #plt.scatter(times, ratios)
    #plt.errorbar(times, ratios[:,0], yerr=ratios[:,1], fmt="o", capsize=3, capthick=2)
    plt.errorbar(times, ratios[:,0], yerr=ratios[:,1], fmt="o", capsize=3, capthick=2)
    plt.xlim(-10, 210)
    plt.ylim(0, lim)
    plt.xlabel("t(m): Mixing Time (ms)")
    plt.ylabel("I$_{12}$/I$_{11}$")
    #plt.title("")
    plt.tight_layout()
    #plt.savefig(f"figures/Iratios_{f_pos}.png", dpi=300, transparent=True)
    plt.show()

#plot_iratios()