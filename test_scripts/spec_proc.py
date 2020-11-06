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
