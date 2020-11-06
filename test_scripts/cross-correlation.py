# Set the correlation velocity resolution and bounds.
# ---------------------------------------------------
dv = 0.15          # Assumed to be in km/s unless provided as an Astropy Unit.

# Set the velocity range for analysis:
# -----------------------------------
VelBound = [-50, 100] # Boundaries for the cross correlation.

obs_list.calc_rv_against_template(template, dv=dv, VelBound=VelBound, err_per_ord=False, combine_ccfs=True, fastccf=True

plt.figure(figsize=(13, 4), dpi= 80, facecolor='w', edgecolor='k')
plt.errorbar(obs_list.time_list,
             obs_list.vels,
             yerr=obs_list.evels,
             fmt='.k')

plt.title('RVs!')
plt.xlabel(r'JD $-$ ${\rm JD}_0$')

plt.ylabel(r'RV [km/s]')
plt.grid()

obs_list.ccf_list[3].plotCCFs()
