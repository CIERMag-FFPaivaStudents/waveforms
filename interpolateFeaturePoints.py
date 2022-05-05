# Author: Gustavo Solcia
# E-mail: gustavo.solcia@usp.br

import numpy as np
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
from scipy.interpolate import PchipInterpolator

"""Creates older adults blood flow waveform feature points from doi:10.1088/0967-3334/26/4/013 and doi:10.1088/0967-3334/31/3/002

"""

def loadFeaturePoints(inputFile):
    """Load relative time (T) and volumetric flow rate (V) from an input csv file.

    Parameters
    ----------
    inputFile: str
        Path to input file + name of feature points csv

    Returns
    -------
    T: array
        Time points relative to time of mid-acceleration.
    V: array
        Normalized volumetric flow rate values.

    """
    data = pd.read_csv(inputFile, delimiter=',', header=None)
    T = (data[0]-1*data[0][0])*1e-3 # conversion from milisecond to second 
    V = data[1]                   # and offset to t=0
    
    return T, V

def interpolateFeatures(t,T,V):
    """Cubic spline interpolation in waveform feature points.

    Parameters
    ----------
    t: array
        Time array to fit interpolation
    T: array
        Time points relative to time of mid-acceleration.
    V: array
        Normalized volumetric flow rate values feature points.

    Returns
    -------
    interpolation: array
        Cubic spline interpolation from feature points.

    """

    fit = PchipInterpolator(T,V)
    interpolation = fit(t)

    return interpolation

def saveFlowRateData(outputName, t, flowRate):
    """Saves time and flow rate data in a csv using pandas dataframe.

    Parameters
    ----------
    outputName: str
        Path to crate output file and csv desired name.
    t: array
        Time array to fit interpolation.
    flowRate: array
        Converted flow rate in cubic meters per second.

    """

    flowRateData = pd.DataFrame({'t': t, 'flow':flowRate})
    flowRateData.to_csv(outputName+'.csv', index=False)

if __name__=='__main__':

    featuresInput = 'data/Hoi-featurePoints-normalized'
    artery = '_ECA'
    outputName = 'Hoi-OlderAdults-Waveform'

    t_0 = 0
    t_f = 1
    dt = 0.0001
    meanFlowRate = 2
    conversionConst = 1e-6/60 #constant of flow rate in m3/s

    t = np.arange(t_0, t_f+dt, dt)

    T_CCA, V_CCA = loadFeaturePoints(featuresInput+artery+'.csv')

    interpCCA = interpolateFeatures(t, T_CCA, V_CCA)

    convertedFlow = meanFlowRate*interpCCA*conversionConst

    saveFlowRateData(outputName+artery, t, convertedFlow)
