from sparta import Observations
import numpy as np

def readNRES(hdul):

    # NRES data has 67 orders
    n_orders, s, w = 67, [], []

    # Read the data from the fits file
    for ordind in np.arange(n_orders):
        s.append(np.array(hdul[2].data[ordind]))
        w.append(10 * np.array(hdul[6].data[ordind])) # NRES gives the data in nm. Convert to Ang.

    # Read the barycentric correction
    bcv = hdul[0].header["RVCC"] - hdul[0].header["RCC"] * 299792.458

    # Read the time of observations
    t   = hdul[0].header["BJD"]

    # There's no metadata to add
    metadata = None

    return t, s, w, n_orders, bcv, metadata

obs_list = Observations(read_function=readNRES, target_visits_lib='/home/darin/Spectral-analysis/SPARTA-master/examples/data/TOI677/')

#print('Time list: {}'.format(obs_list.time_list))
#print('Spec list: {}'.format(obs_list.spec_list))
#print('Time series: {}'.format(obs_list.observation_TimeSeries))
#print('File list: {}'.format(obs_list.file_list))
#print('BCV: {}'.format(obs_list.bcv))
#print('First time: {}'.format(obs_list.first_time))

'''
-----------------------------------------------------------------------
'''

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
plt.ylabel(r'Normalized Intensity')
plt.grid()

#plt.savefig("test_initial_spectrum.pdf")
#plt.show()

'''
---------------------------------------------------------------------
'''

import numpy as np

# Keep only the required orders
selected_ords = [10+I for I in np.arange(40)]
obs_list.SelectOrders(
            selected_ords,
                remove=False)

# Remove NaNs, trim edges, remove cosmics:
# ---------------------------------------
RemoveNaNs = True     # Remove NaN values.
CleanMargins = True   # Cut the edges of the observed spectra. Remove zero padding.
Ntrim = 100           # Number of pixels to cut from each side of the spectrum.
RemCosmicNum = 3      # Number of sigma of outlier rejection. Only points that deviate upwards are rejected.

# Interpolate the spectrum to evenly sampled bins:
# ------------------------------------------------
delta = 0.5           # 0.5 is equivalent to oversampling of fator 2.

# Interpolate the spectrum to evenly sampled bins:
# ------------------------------------------------
FilterLC = 4           # Stopband freq for low-pass filter. In units of the minimal frequency (max(w)-min(w))**(-1)
FilterHC = 0.15        # Stopband freq for the high-pass filter. In units of the Nyquist frequency.
order = 1              # The order of the Butterworth filter (integer)

# Apply cosine-bell:
# ------------------
alpha = 0.3            # Shape parameter of the Tukey window

obs_list.PreProccessSpectra(Ntrim=Ntrim, CleanMargins=CleanMargins, RemoveNaNs=RemoveNaNs,
                                    delta=delta, RemCosmicNum=RemCosmicNum, FilterLC=FilterLC, FilterHC=FilterHC,
                                                                alpha=alpha, verbose=True)

'''
---------------------------------------------------------------------
'''

from sparta.UNICOR.Template import Template

# Retrieve the template.
# If the template is not located in a local directory 
# it will be downloaded from the PHOENIX FTP:
template = Template(temp=5800,
                    log_g=3.5,
                    metal=0.5,
                    alpha=0.0,
                    min_val=4650,
                    max_val=7500,
                    air=False)

# Bin the template, to reduce computational strain:
print('Integrating.', end=' ')
template.integrate_spec(integration_ratio=3)

# Make sure that the data are evenly sampled.
# No over sampling required, so the delta=1 (because when delta<1 sp is oversampled)
print('Interpolating.', end=' ')
template.model.InterpolateSpectrum(delta=1)

# Apply rotational broadening of 6 km/s:
print('Rotating.', end=' ')
template.RotationalBroadening(vsini=6, epsilon=0.5)

# Instrumental broadening for R=53,000
print('Broadening.', end=' ')
template.GaussianBroadening(resolution=53000)

# Cut the template like the observed spectrum
print('Cutting to fit spectra.', end=' ')
template.cut_multiorder_like(obs_list.spec_list[0], margins=150)

# Filter the spectrum Just like the observations were filtered:
template.model.SpecPreProccess(Ntrim=10, CleanMargins=False, RemoveNaNs=False,
                                       delta=1, RemCosmicNum=3, FilterLC=4, FilterHC=0.15, alpha=0.3)

print('Done.')

'''
-------------------------------------------------------------------
'''

# Plot the resulting spectrum
plt.rcParams.update({'font.size': 14})

# plot order 27
plt.figure(figsize=(13, 4), dpi= 80, facecolor='w', edgecolor='k')
ax1 = plt.plot(obs_list.spec_list[0].wv[10], obs_list.spec_list[0].sp[10], 'k', label='Data')
ax2 = plt.plot(template.model.wv[10], template.model.sp[10], 'r', label='Model')

plt.xlabel(r'Wavelength [${\rm \AA}$]')
plt.ylabel(r'Normalized Intensity')
plt.legend()
plt.grid()

#plt.savefig("test_template.pdf")
#plt.show()

'''
-------------------------------------------------------------------
'''

# Set the correlation velocity resolution and bounds.
# ---------------------------------------------------
dv = 0.15          # Assumed to be in km/s unless provided as an Astropy Unit.

# Set the velocity range for analysis:
# -----------------------------------
VelBound = [-50, 100] # Boundaries for the cross correlation.

obs_list.calc_rv_against_template(template, dv=dv, VelBound=VelBound, err_per_ord=False, combine_ccfs=True, fastccf=True)

plt.figure(figsize=(13, 4), dpi= 80, facecolor='w', edgecolor='k')
plt.errorbar(obs_list.time_list,
             obs_list.vels,
             yerr=obs_list.evels,
             fmt='.k')

plt.title('Radial Velocities')
plt.xlabel(r'JD $-$ ${\rm JD}_0$')

plt.ylabel(r'RV [km/s]')
plt.grid()

#plt.savefig("test_rv_time.pdf")

obs_list.ccf_list[3].plotCCFs()

#plt.savefig("test_ccf_curve.pdf")
#plt.show()

