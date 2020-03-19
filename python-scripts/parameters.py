
# Units that we are going to adopt for the different magnitudes

r = 10**10  #cm (radius)
P = 10**15  #din cm−2 (pressure)
T = 10**7   #K (temperatura)
M = 10**33  #g (mass)
L = 10**33  #erg s−1 (luminosity)
rho = 1     #g cm−3 (density)
epsilon = 1 #erg g−1 s−1 (energy rate production)
kappa = 1   #cm2 g−1 (opacity)

# Parameters

X = 0.75      # Hydrogen fraction
Y = 0.22      # Helium fraction
Z = 1 - X - Y # Heavy elements fractio

mu = 1 / (2*X + 0.75*Y + 0.5*Z)

# We define the initial values

RTot = 11.5 # Total radius
LTot = 70   # Total Luminosity
MTot = 5    # Total mass
Tc = 2.0    # Center temperature
Rini = 0.9 * RTot # Initial Radius
h = - Rini / 100  # Step

