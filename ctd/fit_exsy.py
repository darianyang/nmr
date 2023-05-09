"""
Take the intensity ratios over mixing times from an EXSY 
experiment and fit to a curve to extract rate constants.

Fitting to equation 3 in SI: 
https://pubs.acs.org/doi/abs/10.1021/acs.jpclett.9b00052
"""

import numpy as np
import matplotlib.pyplot as plt
import scipy.optimize

#plt.style.use("/Users/darian/github/wedap/wedap/styles/default.mplstyle")
plt.style.use("/Users/darian/github/wedap/styles/poster.mplstyle")

# 4F or 7F
f_pos = "4F"
print(f"CTD-{f_pos}:")

# import intensity ratio dataset (I_12 / I_11)
ratios = np.loadtxt(f"iratios_{f_pos}.txt")
# mixing times (skipping 600ms for now)
times = np.array([2, 5, 10, 15, 25, 35, 50, 75, 100, 200])
# convert ms to seconds
#times = times / 1000

fig, ax = plt.subplots()
#ax.scatter(times, ratios)
ax.errorbar(times, ratios[:,0], yerr=ratios[:,1], fmt="o", capsize=3, capthick=2)
#ax.set(xlabel="Mixing Time(s)", ylabel="I$_{12}$/I$_{11}$", title=f"{f_pos}-CA-CTD")
ax.set(xlabel="Mixing Time(ms)", ylabel="I$_{12}$/I$_{11}$")

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
    param, param_cov = scipy.optimize.curve_fit(calc_iratio, times, ratios[:,0])
    #print("k_12 and k_21:", param)
    #print("cov:", param_cov)
    # top-left to down-right is the leading/main diagonal
    # diagonal of cov matrix is the variance per parameter
    #print("\tdiag:", np.diag(param_cov))
    # sqrt of the variance is the stdev
    p_sigma = np.sqrt(np.diag(param_cov))

    # rate with stdev
    print(f"k_12 = {param[0]:0.2f} ± {p_sigma[0]:0.2f} s^-1")
    print(f"k_21 = {param[1]:0.2f} ± {p_sigma[1]:0.2f} s^-1")

    # exchange ratio
    Kex = param[0] / param[1]
    # propagate the error from division of rates
    # for z = x/y: ∆z/z = sqrt( (∆x/x)^2 + (∆y/y)^2 + ... ) | solving for ∆z
    K_error = Kex * (np.sqrt( (p_sigma[0]/param[0])**2 + (p_sigma[1]/param[1])**2 ))
    print(f"K_ex = {Kex:0.2f} ± {K_error:0.2f}")

    return param, p_sigma

rates, stdevs = calc_rates()

def plot_fitted_curve(ax):
    """
    After curve fitting, plot I(tm) function using the
    fitted rate constants.
    """
    # cover many mixing times from 0-250ms
    #x = np.linspace(0, 0.250, 500)
    x = np.linspace(0, 250, 500000)
    y = np.array([calc_iratio(i, rates[0], rates[1]) for i in x])

    ax.plot(x, y, linestyle="--", color="tab:blue")

plot_fitted_curve(ax)

fig.tight_layout()
fig.savefig(f"figures/fit_exsy_{f_pos}_poster.png", dpi=600, transparent=True)
#plt.show()
