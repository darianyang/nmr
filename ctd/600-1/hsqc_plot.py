"""
Plot 2D HSQC (e.g. 1H-15N) spectra.
"""

import nmrglue as ng
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm
import matplotlib.patches as patches

import plot_peak_labels

plt.style.use("/Users/darian/github/wedap/wedap/styles/default.mplstyle")

# plot parameters
#contour_start = 2400000           # contour level start value
contour_start = 1500000           # contour level start value
#contour_start = 1200000           # contour level start value
contour_num = 8                # number of contour levels
contour_factor = 1.8          # scaling factor between contour levels

# calculate contour levels
cl = contour_start * contour_factor ** np.arange(contour_num) 

def plot_hsqc(path, contour_levels=cl, ax=None, label=None, 
              color="magenta", title=None, linewidths=1.5):
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

    cmap = matplotlib.cm.Blues_r    # contour map (colors to use for contours)

    # plot the contours (tranpose needed here)
    #ax.contour(data.T, contour_levels, cmap=cmap, extent=(ppm_1h_0, ppm_1h_1, ppm_15n_0, ppm_15n_1))
    ax.contour(data.T, contour_levels, colors=color, extent=(ppm_1h_0, ppm_1h_1, ppm_15n_0, ppm_15n_1), 
               linewidths=linewidths)

    if label is not None:
        # Add labels to the legend using dummy plots
        ax.plot([], [], color=color, label=label)

    # add grid at each x and y tick
    ax.grid(color='darkgrey', linestyle='-', linewidth=0.5)

    # decorate the axes
    ax.set_ylabel("$^{15}$N (ppm)")
    ax.set_xlabel("$^{1}$H (ppm)")
    ax.set_title(title)
    ax.set_xlim(6, 11)
    ax.set_ylim(100, 135)
    # the WT rectangle is X: 9.9 - 10.9, Y: 128 - 132.5
    #ax.set_xlim(9.9, 10.9)
    #ax.set_ylim(128, 132.5)
    ax.invert_xaxis()
    ax.invert_yaxis()

fig, ax = plt.subplots(figsize=(11,7))

# WT
#plot_hsqc("DTY_22Feb2024_CA-CTD-WT_2mM_hsqc/4/test.DAT", color="tab:blue", ax=ax, label="WT")
# T188C reduced
plot_hsqc("DTY_22Feb2024_CA-CTD-T188C_2mM_hsqc/1/test.DAT", color="tab:blue", ax=ax, label="T188C RED")

# T188C 'full' red
# plot_hsqc("DTY_22Feb2024_CA-CTD-T188C_2mM_hsqc/1/test.DAT", 
#           color="tab:blue", ax=ax, label="T188C Reduced 1")
# plot_hsqc("DTY_22Feb2024_CA-CTD-T188C_2mM_hsqc/20/test.DAT", 
#           color="tab:red", ax=ax, label="T188C Reduced 2")
# T188C 'full' ox
plot_hsqc("DTY_22Feb2024_CA-CTD-T188C_2mM_hsqc/10/test.DAT", 
          color="tab:green", ax=ax, label="T188C half OX")

# T188C ox some
# plot_hsqc("DTY_22Feb2024_CA-CTD-T188C_2mM_hsqc/2/test.DAT", 
#           color="tab:red", ax=ax, label="T188C Oxidized 1")
# plot_hsqc("DTY_22Feb2024_CA-CTD-T188C_2mM_hsqc/3/test.DAT", 
#           color="tab:red", ax=ax, label="T188C Oxidized 2")
# plot_hsqc("DTY_22Feb2024_CA-CTD-T188C_2mM_hsqc/5/test.DAT", 
#           color="tab:red", ax=ax, label="T188C Oxidized 3")
# plot_hsqc("DTY_22Feb2024_CA-CTD-T188C_2mM_hsqc/6/test.DAT", 
#           color="tab:green", ax=ax, label="T188C Oxidized 4")

# T188C ox 20uM
# cl = 3000000 * contour_factor ** np.arange(contour_num) 
# plot_hsqc("DTY_22Feb2024_CA-CTD-T188C_2mM_hsqc/30/test.DAT", cl,
#           color="tab:green", ax=ax, label="T188C OX 20$\mu$M")

# post Cu dialysis full ox
cl = 2400000 * contour_factor ** np.arange(contour_num) 
plot_hsqc("DTY_22Feb2024_CA-CTD-T188C_2mM_hsqc/40/test.DAT", cl,
          color="tab:red", ax=ax, label="T188C OX",)

# current WT spectrum compare to previous, 
# maybe older WT is oxidized and that's why there is shifts?
# nope, looks the same
# cl = 1200000 * contour_factor ** np.arange(contour_num) 
# plot_hsqc("../800/DTY-CaCTD-15NFW-12162022/1/test.DAT", cl,
#           color="tab:red", ax=ax, label="T188C WT Pre")

# peak label plotting function
# 4F
#shifted = [176, 172, 185, 183, 174, 190, 182, 180, 174, 192, 177, 179]
#plot_peak_labels.peak_text_plotter("CA_CTD_BMRB_assignments.shifts", ax=ax, redlist=shifted)
# 7F
#shifted = [182, 185, 184, 186]
#plot_peak_labels.peak_text_plotter("CA_CTD_BMRB_assignments.shifts", ax=ax, redlist=shifted)

#ax.set_title("CTD WT vs 7F")
# ax.set_title("CA-CTD WT $^1$H-$^{15}$N HSQC")
#ax.set_title("CA-CTD WT W184 N$\epsilon$")

# Create a Rectangle patch for zoom on WT CTD HSQC
# rect = patches.Rectangle((9.9, 128), 0.9, 4.5, linewidth=1.5, edgecolor="k", facecolor="none")
# # Add the patch to the Axes
# ax.add_patch(rect)
# # so the rectangle is X: 9.9 - 10.9, Y: 128 - 132.5

# cysteines
#plot_peak_labels.peak_text_plotter("../CA_CTD_BMRB_assignments.shifts", ax=ax, redlist=[188, 198, 218])
# WT vs T188C
# plot_peak_labels.peak_text_plotter("../CA_CTD_BMRB_assignments.shifts", ax=ax, 
#                                    redlist=[150,220,186,210,193,190,209,184,146,187,213,177,215,216,148,192,191,199,206])
# T188C red vs ox
# plot_peak_labels.peak_text_plotter("../CA_CTD_BMRB_assignments.shifts", ax=ax, 
#                                    redlist=[156,162,206,218,186,210,150,195,161,194,146,148,153,189,187,205])
# gradual oxidation comparison
# plot_peak_labels.peak_text_plotter("../CA_CTD_BMRB_assignments.shifts", ax=ax, 
#                                    redlist=[])

# full oxidation comparison
plot_peak_labels.peak_text_plotter("../CA_CTD_BMRB_assignments.shifts", ax=ax,
                                  redlist=[161,199,169,162,182,222,191,201,155,174,186,220,218,188,148,172,150,168,179,200,152,184,216,146,194,198])

plt.legend(frameon=False)
fig.tight_layout()
plt.show()
#fig.savefig("figures/wt_vs_7f_hsqc_peak_labels.png", dpi=300, transparent=True)
#fig.savefig("figures/wt_hsqc_boxonly.png", dpi=300, transparent=True)
#fig.savefig("WT_vs_T188C_shifts.pdf")
#fig.savefig("T188C_red_vs_ox_shifts.pdf")
#fig.savefig("T188C_red_vs_ox4_shifts.pdf")
#fig.savefig("T188C_ox_conc_100x.pdf")
#fig.savefig("WT_pre_vs_post_freeze.pdf")
#fig.savefig("T188C-post-Cu-ox.pdf")