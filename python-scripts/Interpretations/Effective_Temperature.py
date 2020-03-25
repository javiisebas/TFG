from Final_Model_Parameters import *
from numpy import pi

# We defin a function to calculate then effective temperature
def Teff(L, R):

    SB = 5.6704 * 10**-5
    return (L / (4 * pi * R**2 * SB)) ** 0.25

Teff_Model = Teff(L_Model, R_Model)

print("Effective Temperature = {:.2f} K".format(Teff_Model))
