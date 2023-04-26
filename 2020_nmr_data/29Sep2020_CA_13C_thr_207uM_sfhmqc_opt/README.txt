These experiments were done after taking CA fl with 13C Ala and 13C Thr
labels, and transfering them to 100% D2O buffer from H2O.
This was in an effort to get better water supression and overall S/N.

Testing sf-hmqc on NMR 600-1

sfHMQC and ct-HSQC data were obtained for 13C Thr CA 207uM on NMR 600-1

Conditions:
25mM NaPi, pH 6.5, 0.02% NaN3, 1mM DTT/TCEP

29Sep2020_CA_13C_thr_207uM_sfhmqc_opt:
exp 1-6: S/N opt sf-hmqc
1s d1 relaxation delay
71ms aquisition time (aq)
carrier freq set to 1.2ppm (thr) instead of 4.7ppm (water)
90 deg flip pulse is better than 30 deg (P50=6ms instead of 2ms)

exp 11-13: sf-hmqc d1 1ms vs sf-hmqc d1 1s vs cthsqc overnight (~5hr each)
* had incorrect PL29 value, cause peak splitting

exp 21-24: d1=1s vs d1=1ms vs d1=1ms,30deg vs ct-hsqc
20 minutes each with corrected PL29 value (-7.29)
result - d1 of 1s lead to best S/N


