import numpy as np
import pandas as pd
import sklearn.neighbors.kde import KernelDensity

'''
Marchenko–Pastur's law describes the asymptotic behavior of values in large
rectangular random matrices. See:
https://en.wikipedia.org/wiki/Marchenko%E2%80%93Pastur_distribution


Given it proves the minimum and maximum expected eigenvalues of a random,
rectangular matrix, values outside of [eMin, eMax] are consistent with
non-random behavior.

The Marchenko–Pastur Probability Density Function:
'''
def mpPDF(variance, q, pts):
  eMin = variance * (1 - (1.0 / q)**0.5)**2
  eMax = variance * (1 + (1.0 / q)**0.5)**2
  eVals = np.linspace(eMin, eMax, pts)
  pdf = q / (2*np.pi*variance*eVals)*((eMax-eVals)*(eVals-eMin))**0.5
  return pd.Series(pdf, index=eVals)

