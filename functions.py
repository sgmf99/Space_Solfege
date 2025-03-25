import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import astropy.units as u
import astropy.constants as C
from astropy.io import fits
import pdb


"""
Sofi Martínez Fortis
--------------------
Functions used in Midterm_Project.ipynb
"""


def angs2Hz(lam):
    """
    SGMF: converts wavelength into frequency

    Parameters:
    -----------
    lam: wavelength or array of wavelengths (in Angstroms)

    Returns:
    --------
    f: frequency (in 1/s)
    """

    lam = lam*u.AA
    f = C.c/lam
    return f.cgs


def Hz2angs(f):
    """
    SGMF: converts frequency into wavelength

    Parameters:
    -----------
    f: frequency or array of frequencies (in 1/s)

    Returns:
    --------
    lam: wavelength (in Angstroms)
    """

    lam = C.c/f
    return lam.to(u.AA)


def redshift(lrest, lobs):
    """
    SGMF: Computes redshift needed to observe wavelength, lrest, at wavelength, lobs

    Parameters:
    -----------
    lrest: rest wavelength (in Angstroms)
    Lobs: observed wavelength (in Angstroms)

    Returns:
    --------
    z: redshift
    """
    z = (lobs - lrest)/lrest
    return z


def freq_ratios():
    """
    SGMF: 
    -----
    Compute the frequency ratios:
        Do:Re (P1:M2)
        Do:Mi (P1:M3)
        Do:Fa (P1:P4)
        Do:Sol (P1:P5)
        Do: La (P1:M6)

    I assume Do is C0 (16.35 Hz) for these calculations so that ratios are as follows:
        C0:D0
        C0:E0
        C0:F0
        C0:G0
        C0:A0

    Frequencies are taken from 
    https://mixbutton.com/music-tools/frequency-and-pitch/music-note-to-frequency-chart

    """

    ratios = 16.35/np.array([18.35, 20.60, 21.83, 24.50, 27.50])

    return ratios





def main():

    # SGMF: 
    # find frequencies and wavelengths corresponding to intervals (M2, M3, P4, P5, M6)
    # assuming H alpha (6563 Ang) is 'Do'
    ratios = freq_ratios()
    Ha_f = angs2Hz(6562.7) # H alpha frequency
    freqs = Ha_f/ratios
    lams = Hz2angs(freqs)

    # SGMF:
    # Find z needed to achieve lams
    # Lines of interest:
        # M2: Mg I 5175
        # M3: Mg I 5175
        # P4: H beta
        # P5: H gamma
        # M6: H zeta
    lrests = np.array([5175, 5175, 4861, 4340, 3889])*u.AA # SGMF: rest wavelengths corresponding to each line
    zs = redshift(lrests, lams)

    df = pd.DataFrame({
        'f ratio': ratios,
        'Line': ['Mg I 5175', 'Mg I 5175', "H\u03B2", "H\u03B3", "H\u03B6"],
        "\u03BB_rest": lrests,
        "\u03BB_obs": lams,
        'z': zs
    }, index=['M2', 'M3', 'P4', 'P5', 'M6'])

    
    # df.style.set_caption(r"Do: H$\alpha \, (6563 \AA)$")
    df = df.round({'f ratio': 3, "\u03BB_rest": 0, "\u03BB_obs": 0, 'z': 4})
    df.to_csv('Data/interval_info.csv', index=True)

if __name__=='__main__':
    main()
    

