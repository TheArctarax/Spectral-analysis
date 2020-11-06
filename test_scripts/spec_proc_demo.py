import copy as cp
import matplotlib.pyplot as plt

# Choose a specifiec observation
spec = cp.deepcopy(obs_list.spec_list[5])

# Remove cosmics, NaNs and zero paddings:
spec.SpecPreProccess(Ntrim=100, CleanMargins=True, RemoveNaNs=True,
                     delta=0.5, RemCosmicNum=3, FilterLC=4, FilterHC=0.15, alpha=0.3)

# Plot the resulting spectrum
plt.rcParams.update({'font.size': 14})

# plot order 27
plt.figure(figsize=(13, 4), dpi= 80, facecolor='w', edgecolor='k')
plt.plot(spec.wv[20], spec.sp[20], 'k')
plt.xlabel(r'Wavelength [${\rm \AA}$]')
plt.ylabel(r'Normazlied Intensity')
plt.grid()
