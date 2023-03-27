"""
Plot 1D (e.g. 19F) spectra.
"""

import nmrglue as ng
import matplotlib.pyplot as plt
import numpy as np

#plt.style.use("/Users/darian/github/wedap/wedap/styles/default.mplstyle")

def plot_1d(path, ax=None, label=None, color="magenta", scale=None, xlim=(-120, -140)):
    """
    Plot 1D NMR spectrum.

    Parameters
    ----------
    path : str
        Path to nmr data file (e.g. nmrpipe).
    ax : mpl axes object
    label : str
        Plot label
    color : str
        Plot color
    scale : int
        Multiply data to scale if comparing across multiple concentrations.
    xlim : tuple of ints/floats
    """
    if ax is None:
        fig, ax = plt.subplots()
    else:
        fig = plt.gcf()

    # read in the data from a NMRPipe file
    dic,data = ng.pipe.read(path)
    
    print(data.shape)

    # print intensity of d1 and d2 peaks
    peaks = ng.peakpick.pick(data, 21000000)
    #peaks = ng.peakpick.pick(data, 10000000)
    print(peaks)
    p1 = peaks[0][0]
    p2 = peaks[2][0]
    print("Peak Intensities:", data[int(p1)], data[int(p2)])
    # Kd = [D2] / [D1]
    print("\t\t  Kd = ", data[int(p2)] / data[int(p1)])

    # get the error of the peak intensity ratio from peak 1 height and SNR
    # rmsd of the noise for a non-signal region
    # sqrt(1/n * (x_1^2 + x_2^2 + ... + x_n^2))
    noise = data[:4000]
    rmsnoise = np.sqrt(np.sum(noise**2) / noise.shape[0])

    # snr = peak_height / rms noise
    snr_p1 = data[int(p1)] / rmsnoise
    #print(snr_p1)
    
    # intensity ratio
    iratio = data[int(p2)] / data[int(p1)]

    # abs uncertainty from random noise in ratio of peak heights (∆R)
    # |ΔR| = 1/SNR_B + R/SNR_B where R = A/B
    dR = (1/snr_p1) + (iratio/snr_p1)
    print(dR)

    # optionally scale data for different concentrations
    if scale:
        data *= scale

    # create a unit conversion object for the axis
    uc = ng.pipe.make_uc(dic, data)

    # plot the spectrum
    ax.plot(uc.ppm_scale(), data, color=color, label=label)

    # decorate axes
    ax.set_yticklabels([])
    ax.set_yticks([])
    #ax.set_title("CTD $^{19}$F 1D")
    ax.set_xlabel("$^{19}$F (ppm)", fontsize=12, labelpad=10, fontweight="bold")
    ax.set_xlim(xlim[0], xlim[1])
    #ax.set_ylim(-80000, 2500000)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    #ax.invert_xaxis()

    # save the figure
    #fig.savefig("spectrum.png") # this can be .pdf, .ps, etc

# 4F or 7F
f_pos = "4F"
fig, ax = plt.subplots()

#plot_1d(f"600-2/DTY-CaCTD-F-12152022/1/test.DAT", ax=ax, label={f_pos}, color="black")
# plot_1d("600-2/DTY-CaCTD-F-12152022/2/test.DAT", ax=ax, label=f"{f_pos} 1200µM", color="magenta")
# plot_1d("600-2/DTY-CaCTD-F-12152022/3/test.DAT", ax=ax, label=f"{f_pos} 120µM", color="k", scale=10, xlim=(-117, -135))
# ax.invert_xaxis()
# plt.legend(prop={'size': 12})

plot_1d("600-2/DTY-CaCTD-F-12152022/2/test.DAT", ax=ax, label=f"{f_pos}", xlim=(-120, -131.5))
#plot_1d("600-2/DTY-CaCTD-F-12152022/1/test.DAT", ax=ax, label=f"{f_pos}", xlim=(-140, -127))
#plot_1d("600-2/DTY-CaCTD-F-12152022/23/test.DAT", ax=ax, label=f"{f_pos}", xlim=(-140, -127))

fig.tight_layout()
#plt.show()
fig.savefig(f"figures/1d_ctd_{f_pos}_1024NS.svg", dpi=300, transparent=True)