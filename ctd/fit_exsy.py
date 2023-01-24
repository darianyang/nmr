"""
Take the intensity ratios over mixing times from an EXSY 
experiment and fit to a curve to extract rate constants.

Fitting to equation 3 in SI: 
https://pubs.acs.org/doi/abs/10.1021/acs.jpclett.9b00052
"""

import numpy as np
import matplotlib.pyplot as plt
import scipy.optimize

plt.style.use("/Users/darian/github/wedap/wedap/styles/default.mplstyle")

# 4F or 7F
f_pos = "7F"

# import intensity ratio dataset (I_12 / I_11)
ratios = np.loadtxt(f"iratios_{f_pos}.txt")
# mixing times (skipping 600ms for now)
times = np.array([2, 5, 10, 15, 25, 35, 50, 75, 100, 200])
# convert ms to seconds
times = times / 1000

fig, ax = plt.subplots()
ax.scatter(times, ratios)
ax.set(xlabel="Time(s)", ylabel="I$_{12}$/I$_{11}$", title=f"{f_pos}-CA-CTD")

def calc_iratio(t_m, k_12, k_21):
    """
    Calculates (I_12 / I_11) as a function of mixing time.
    """
    return ((1 - np.exp(-(k_12 + k_21) * t_m)) * k_12) / \
        (k_21 + k_12 * np.exp(-(k_12 + k_21) * t_m))

#print(calc_iratio(0.2, 74, 114))

def calc_rates():
    """
    Using intensity ratios per mixing time, use lls fitting from
    scipy.curve_fit to optimize rate constants in I(tm).
    """
    # fit to estimate k_12 and k_21, using 1 as initial guess
    param, param_cov = scipy.optimize.curve_fit(calc_iratio, times, ratios)
    print("k_12 and k_21:", param)

    return param

rates = calc_rates()
Kd = rates[0] / rates[1]
print(f"\t\tKd = {Kd}")

def plot_fitted_curve(ax):
    """
    After curve fitting, plot I(tm) function using the
    fitted rate constants.
    """
    # cover many mixing times from 0-250ms
    x = np.linspace(0, 0.250, 500)
    y = np.array([calc_iratio(i, rates[0], rates[1]) for i in x])

    ax.plot(x, y, linestyle="--")

plot_fitted_curve(ax)

fig.tight_layout()
fig.savefig(f"figures/fit_exsy_{f_pos}.png", dpi=300, transparent=True)
plt.show()