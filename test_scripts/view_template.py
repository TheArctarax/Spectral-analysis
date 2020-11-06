# Plot the resulting spectrum
plt.rcParams.update({'font.size': 14})

# plot order 27
plt.figure(figsize=(13, 4), dpi= 80, facecolor='w', edgecolor='k')
ax1 = plt.plot(obs_list.spec_list[0].wv[10], obs_list.spec_list[0].sp[10], 'k', label='Data')
ax2 = plt.plot(template.model.wv[10], template.model.sp[10], 'r', label='Model')

plt.xlabel(r'Wavelength [${\rm \AA}$]')
plt.ylabel(r'Normazlied Intensity')
plt.legend()
plt.grid()
