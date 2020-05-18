
'''
 This library is compouse of the units that we are going to adopt for the different magnitudes
'''

# Magnitudes

r = 10**10  #cm (radius)
P = 10**15  #din cm−2 (pressure)
T = 10**7   #K (temperatura)
M = 10**33  #g (mass)
L = 10**33  #erg s−1 (luminosity)
rho = 1     #g cm−3 (density)
epsilon = 1 #erg g−1 s−1 (energy rate production)
kappa = 1   #cm2 g−1 (opacity)


# Parameters

X = 0.80      # Hydrogen fraction
Y = 0.16      # Helium fraction
Z = 1 - X - Y # Heavy elements fraction
 
mu = 1 / (2*X + 0.75*Y + 0.5*Z) # mu - reduce mass

MTot = 5                        # Total radius
RTot_initial = 12               # Initial Radius
LTot_initial = 40               # Initial Luminosity
layers = 100                    # Number of layers in the star
