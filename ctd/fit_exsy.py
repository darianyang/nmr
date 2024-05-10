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
#plt.style.use("/Users/darian/github/wedap/styles/poster.mplstyle")

# 4F or 7F
f_pos = "4F"
print(f"CTD-{f_pos}:")

fig, ax = plt.subplots()

# import intensity ratio dataset (I_12 / I_11)
ratios = np.loadtxt(f"iratios_{f_pos}.txt")
# mixing times (skipping 600ms for now)
times = np.array([2, 5, 10, 15, 25, 35, 50, 75, 100, 200])
# convert ms to seconds
#times = times / 1000

def calc_iratio(t_m, k_12, k_21):
    """
    Calculates (I_12 / I_11) as a function of mixing time.
    """
    return ((1 - np.exp(-(k_12 + k_21) * t_m)) * k_12) / \
           (k_21 + k_12 * np.exp(-(k_12 + k_21) * t_m))

#print(calc_iratio(0.2, 74, 114))

def calc_rates(times, ratios):
    """
    Using intensity ratios per mixing time, use lls fitting from
    scipy.curve_fit to optimize rate constants in I(tm).
    """
    # fit to estimate k_12 and k_21, using 1 as initial guess
    param, param_cov = scipy.optimize.curve_fit(calc_iratio, times, ratios)
    #print("k_12 and k_21:", param)
    #print("cov:", param_cov)
    # top-left to down-right is the leading/main diagonal
    # diagonal of cov matrix is the variance per parameter
    print("\tdiag:", np.diag(param_cov))
    # sqrt of the variance is the stdev
    p_sigma = np.sqrt(np.diag(param_cov))

    # rate with stdev
    print(f"k_12 = {param[0]*1000:0.2f} ± {p_sigma[0]*1000:0.2f} ms^-1")
    print(f"k_21 = {param[1]*1000:0.2f} ± {p_sigma[1]*1000:0.2f} ms^-1")

    # exchange ratio
    Kex = param[0] / param[1]
    # propagate the error from division of rates
    # for z = x/y: ∆z/z = sqrt( (∆x/x)^2 + (∆y/y)^2 + ... ) | solving for ∆z
    K_error = Kex * (np.sqrt( (p_sigma[0]/param[0])**2 + (p_sigma[1]/param[1])**2 ))
    print(f"K_ex = {Kex:0.2f} ± {K_error:0.2f}")

    return param, p_sigma, K_error

rates, stdevs, K_error = calc_rates(times, ratios[:,0])
#import sys ; sys.exit(0)

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

# MC bootstrapping error:
def mc_bootstrapping(intensity_ratios, mixing_times, calculate_statistic=np.mean):
    # Number of bootstrap samples
    num_bootstraps = 1000

    # # Function to calculate statistic of interest (mean, median, etc.)
    # def calculate_statistic(data):
    #     return np.mean(data)
    # TODO: calc fitting error from EXSY

    # Perform Monte Carlo bootstrapping
    bootstrap_statistics = []
    for _ in range(num_bootstraps):
        # Resample with replacement
        indices = np.random.choice(len(intensity_ratios), len(intensity_ratios), replace=True)
        resampled_data = intensity_ratios[indices]
        
        # Calculate statistic of interest
        statistic = calculate_statistic(resampled_data)
        bootstrap_statistics.append(statistic)

    # Calculate error bars (e.g., 95% confidence interval)
    confidence_interval = np.percentile(bootstrap_statistics, [2.5, 97.5])

    print("95% Confidence Interval:", confidence_interval)
    return confidence_interval

#mcCI = mc_bootstrapping(ratios, times)
#print(np.array(mcCI).reshape(2,-1))

#import sys ; sys.exit(0)

#ax.scatter(times, ratios)
# error from S/N propagation
ax.errorbar(times, ratios[:,0], yerr=ratios[:,1], fmt="o", capsize=3, capthick=2)
# error from fitting
#ax.errorbar(times, ratios[:,0], yerr=K_error, fmt="o", capsize=3, capthick=2)
# error from MC bootstrapping
#ax.errorbar(times, ratios[:,0], yerr=np.array(mcCI).reshape(2,-1), fmt="o", capsize=3, capthick=2)

#ax.set(xlabel="Mixing Time (s)", ylabel="I$_{12}$/I$_{11}$", title=f"{f_pos}-CA-CTD")
ax.set(xlabel="t(m): Mixing Time (ms)", ylabel="I$_{12}$/I$_{11}$")

fig.tight_layout()
fig.savefig(f"figures/fit_exsy_{f_pos}_final.png", dpi=600, transparent=True)
plt.show()
