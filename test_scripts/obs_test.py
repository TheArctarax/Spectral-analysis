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

obs_list = Observations(read_function=readNRES, target_visits_lib='~/Spectral-analysis/SPARTA-master/examples/data/TOI677/')
#print('Calculate PDC: {}'.format(obs_list.calc_PDC))
print('Time list: {}'.format(obs_list.time_list))
print('Spec list: {}'.format(obs_list.spec_list))
print('Time series: {}'.format(obs_list.observation_TimeSeries))
#print(obs_list.rad_list)
print('File list: {}'.format(obs_list.file_list))
print('BCV: {}'.format(obs_list.bcv))
#print(obs_list.data_type)
print('First time: {}'.format(obs_list.first_time))
