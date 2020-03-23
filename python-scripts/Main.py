
from Parameters_Study import * # We import all the parameters that we have defined

# We want to calculate the center temperature, radius and luminosity that minimize the relative erro
parameters_frontier = frontierStudy(2) # We study our parameters in the frotier

# Ones we have it, we extract the parameters that we are going to use
Tc = parameters_frontier[0]    # Center Temperature
Rfin = parameters_frontier[10] # Radius
Lfin = parameters_frontier[11] # Luminosity

# Running the following function it will print all the parameters in each shell
minRelError(Tc, Rfin, Lfin, True) # We asign True to the variable control, in order to print the parameters
