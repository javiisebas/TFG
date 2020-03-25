
from Initial_Parameters import * # We import all the parameters that we have defined
from numpy import sqrt           # We import the function square root to use it afterwards


# Here we will define all the usefull functions


#-------------------------------------FUNCTIONS TO CALCULATE EPSILON-------------------------------------
# We define a function to study if the temperature is inside the interval
def inside(T1, T2, T):
    '''
    Study whether a temperature is within a range
    Inputs: Temperature inteval and the temperature that we want to study
    Output: False if it is not inside, True if is inside
    '''
    check = False # Initial consideration
    if T >= T1 and T <= T2: # If it is inside, it will change the initial consideration
        check = True
    return check

# Energy rate production for p-p chain
# Interval -> [T1, T2, log_10(epsilon), nu]
interval_PP = [
    [4.0, 6.0, -6.84, 6.0],
    [6.0, 9.5, -6.04, 5.0],
    [9.5, 12.0, -5.56, 4.5], 
    [12.0, 16.5, -5.02, 4.0], 
    [16.5, 24.0, -4.40, 3.5] 
]

# Function for the energy rate production for the p-p chain
def epsilonPP(T):
    '''
    Study the value of epsilon for a certain temperatura for the p-p chain
    Input: Temperature that we want to study
    Output: Value of the energy rate production
    '''

    global X, rho, interval_PP
    
    T *= 10      # First we have to adjust the units
    nu = 0       # Initial nu
    epsilon1 = 0 # Initial epsilon1
    X1 = X2 = X  # Initial composition
    for interval in interval_PP: # We can study if the temperature is within any range
        if inside(interval[0], interval[1], T): # If it is inside the interval, it will change the values of nu and epsilon1
            epsilon1 = 10**interval[2] # New epsilon1
            nu = interval[3]           # New nu
    return epsilon1 * X1 * X2 * rho * T ** nu

# Energy rate production for CNO cycle
# Interval -> [T1, T2, log_10(epsilon), nu]
interval_CNO = [
    [12.0, 16.0, -22.2, 20],
    [16.0, 22.5, -19.8, 18],
    [22.5, 27.5, -17.1, 16],
    [27.5, 36.0, -15.6, 15],
    [36.0, 50.0, -12.5, 13]
]

# Function for the energy rate production for the CNO cycle
def epsilonCNO(T):
    '''
    Study the value of epsilon for a certain temperatura for the p-p chain
    Input: Temperature that we want to study
    Output: Value of the energy rate production
    '''

    global X, Z, rho, interval_CNO
    
    T *= 10      # First we have to adjust the units
    nu = 0       # Initial nu
    epsilon1 = 0 # Initial epsilon1
    X1 = X       # Initial composition
    X2 = Z/3     # Initial compositon
    for interval in interval_CNO: # We can study if the temperature is within any range
        if inside(interval[0], interval[1], T): # If it is inside the interval, it will change the values of nu and epsilon1
            epsilon1 = 10**interval[2] # New epsilon1
            nu = interval[3]           # New nu
    return epsilon1 * X1 * X2 * rho * T ** nu

# Finally the energy rate production will be the biggest between th p-p chain and th CNO cycle
def Epsilon(T):
    '''
    Study which energy rate production is greater, the CNO cycle or the p-p chain
    Input: Temperature that we want to study
    Output: Value of the energy rate production
    '''

    return max(epsilonPP(T), epsilonCNO(T))

# For the value plotting we can define a function that gives us the leading production kind
def Dom_epsilon(T):
    '''
    Study which energy rate production is greater, the CNO cycle or the p-p chain
    Input: Temperature that we want to study
    Output: What kind of energy rate production is leading
    '''

    epsilon = max(epsilonPP(T), epsilonCNO(T))
    
    if epsilon == 0: # If epsilon is zero
        return "--"
    elif epsilon == epsilonPP(T): # If the p-p chain leads
        return "PP"
    else: # If the CNO cycle leads
        return "CN"
#--------------------------------------------------------------------------------------------------------


# We define a function to calculate the relative error
def relError(cal, est):
    '''
    Study the relative error between a calculated value and an estimated value
    Inputs: the calculated and the estimated value
    Output: True if the relative error is lower than or maximun expectin value and False in the opposite case
    '''
    check = False # Initial consideration (Repeat the calculation)
    maximum = 0.0001 # Maximum relative error that we want to get
    if abs(cal - est) / cal < maximum:
        check = True # In case it is lower than the maximum (Not repeating the calculation)    
    return check


#-------------------------FUNCTIONS FOR PHYICAL PARAMETERS (RADIOACTIVITE PHASES)------------------------
# We are going to define the functions to calculate the different physical parameters
# First the functions for the first derivative of the parameters

# Mass first derivative
def M_fi_rad(P, T, r):
    '''
    Study of the mass first derivative
    Input: Pressure, Temperature and Radius
    Output: Value of fi_M
    '''
    global mu
    return 0.01523 * mu * P * r**2 / T

# Presure first derivative
def P_fi_rad(P, T, r, M):
    '''
    Study of the pressure first derivative
    Input: Pressure, Temperature, Radius and Mass
    Output: Value of fi_P
    '''
    global mu
    return -1 * 8.084 * mu * P * M / (T * r**2)

# Temperture first derivative
def T_fi_rad(P, T, r, L):
    '''
    Study of the temperature first derivative
    Input: Pressure, Temperature, Radius and Luminosity
    Output: Value of fi_T
    '''
    global mu, Z, X
    return -1 * 0.01679 * Z * (1+X) * mu**2 * P**2 * L / (T**8.5 * r**2)

# Luminosity first derivative
def L_fi_rad(P, T, r):
    '''
    Study of the luminosity first derivative
    Input: Pressure, Temperature and Radius
    Output: Value of fi_L
    '''
    global mu, Epsilon
    return 0.01845 * Epsilon(T) * mu**2 * P**2 * r**2 / T**2


# Then we define the functions to calculate the T(r) and P(T)
# We will use this functions for the first three shells

# Temperature in a certain shell
def T_rad_fun(r, RTot):
    '''
    Study of the temperature in a certain shell
    Input: Radius of the shell and the total Radius of the star
    Output: Value of T(r)
    '''
    global MTot, mu
    return 1.9022 * mu * MTot * ((1/r) - (1/RTot))

# Pressure in a certain shell
def P_rad_fun(T, LTot):
    '''
    Study of the pressure in a certain shell
    Input: Temperature of the shell and the total Luminosity of the star
    Output: Value of P(r)
    '''
    global mu, Z, X, MTot
    return 10.645 * T**4.25 * sqrt(MTot/(mu * Z * LTot * (1 + X)))
#--------------------------------------------------------------------------------------------------------


#-------------------------------FUNCTIONS FOR ESTIMATED PHYICAL PARAMETERS-------------------------------
# We define:
# Estimated Pressure
def P_est_fun(Pi, fi_P, h):
    '''
    Study of the estimated pressure in a certain shell
    Input: Pressure of the shell, list of pressure first derivative and the step between shells 
    Output: Value of Estimated Pressure 
    '''
    fi = fi_P[-1]
    fi_1 = fi_P[-2]
    fi_2 = fi_P[-3]
    return Pi + (h/12) * (23*fi - 16*fi_1 + 5*fi_2)

# Estimated Temperatere
def T_est_fun(Ti, fi_T, h):
    '''
    Study of the estimated temperature in a certain shell
    Input: Temperature of the shell, list of temperature first derivative and the step between shells 
    Output: Value of Estimated Temperature
    '''
    fi = fi_T[-1]
    fi_1 = fi_T[-2]
    return Ti + (h/2) * (3*fi - fi_1)

# Calculated Pressure, Temperature and Mass
def Gen_cal_fun(Xi, fi1_X, fi_X, h):
    '''
    Study of the calculated pressure, temperature or mass in a certain shell
    Input: Parameter value of the shell, list of parameter values first derivative and the step between shells 
    Output: Value of Calculated Pressure, Temperature or Mass
    '''
    fi1 = fi1_X
    fi = fi_X[-1]
    return Xi + (h/2) * (fi1 + fi)

# Calculated Luminosity
def L_cal_fun(Li, fi1_L, fi_L, h):
    '''
    Study of the calculated luminosity in a certain shell
    Input: Luminosity of the shell, list of luminosity first derivative and the step between shells 
    Output: Value of Calculated Luminosity
    '''
    fi1 = fi1_L
    fi = fi_L[-1]
    fi_1 = fi_L[-2]
    return Li + (h/12) * (5*fi1 + 8*fi - fi_1)
#--------------------------------------------------------------------------------------------------------


# We are going to define n+1:
def n_fun(T_cal, P_cal, fi1_P, fi1_T):
    '''
    Study the value of the parameter that gives us information about the radioactive or convective behavior
    Input: Calculated Temperature and Pressure of the shell, pressure and temperature first derivative of the shell
    Output: Value of the n-parameter 
    '''
    return (T_cal * fi1_P) / (P_cal * fi1_T)


# Function that checks if the condition of radioactive surface is valid
def check_n_fun(n):
    '''
    Study if the n-parameter that we have calculated is in the radioactive range or not
    Input: value of the n-parameter
    Output: True if we are still in the radioactive behavior, and False if we are in the convective behavior
    '''
    
    check = True # If it is True it is still in the radioactive behavior
    if n <= 2.5:
        check = False # If it is False it is now in the convective behavior
    return check


# We can define a function to calculate all the interpolations
def interpolation(y0,y1,n0,n1):
    '''
    Generates a linear interpolation
    Input: two pairs of values (x,y) to make the linear intepolation
    Output: The value interpolated for n=2.5
    '''
    n = 2.5
    return y0 + ((y1 - y0) / (n1 - n0)) * (n - n0)


#---------------------------FUNCTIONS FOR PHYICAL PARAMETERS (CONVECTIVE PHASE)--------------------------
# We are going to define the equations to obtain the parameters in the convective core
# First the functions for the first derivative of the parameters

def M_fi_conv(T, r, K):
    '''
    Study of the mass first derivative
    Input: Temperature, Radius and Polytrope model constant
    Output: Value of fi_M
    '''
    global mu
    return 0.01523 * mu * K * T**1.5 * r**2


def P_fi_conv(T, r, M, K):
    '''
    Study of the pressure first derivative
    Input: Temperature, Radius, Mass and Polytrope model constant
    Output: Value of fi_P
    '''
    global mu
    return -1 * 8.084 * mu * K * T**1.5 * M / r**2


def T_fi_conv(M, r):
    '''
    Study of the temperature first derivative
    Input: Mass and Radius
    Output: Value of fi_T
    '''
    global mu
    return -1 * 3.234 * mu * M / r**2


def L_fi_conv(T, r, K):
    '''
    Study of the luminosity first derivative
    Input: Temperature, Radius and the Polytrope model constant
    Output: Value of fi_L
    '''
    global mu, Epsilon
    return 0.01845 * Epsilon(T) * mu**2 * K**2 * T**3 * r**2

# Then we define the functions to calculate the T(r) and P(T)
# We will use this functions for the first three shells

# Mass(r)
def M_conv(r, K, Tc):
    '''
    Study of the mass in a certain shell
    Input: Radius ,Polytrope model constant and center Temperature
    Output: Value of M(r)
    '''
    global mu
    return 0.005077 * mu * K * Tc**1.5 * r**3

# Luminosity(r)
def L_conv(r, K, Tc):
    '''
    Study of the luminosity in a certain shell
    Input: Radius, the Polytrope model constant and center Temperature
    Output: Value of L(r)
    '''
    global mu, Epsilon    
    return 0.00615 * Epsilon(Tc) * mu**2 * K**2 * Tc**3 * r**3

# Temperature(r)
def T_conv(r, K, Tc):
    '''
    Study of the temperature in a certain shell
    Input: Radius, the Polytrope model constant and center Temperature
    Output: Value of T(r)
    '''
    global mu 
    return Tc - (0.008207 * mu**2 * K * Tc**1.5 * r**2)

# Pressure(r)
def P_conv(r, T, K): 
    '''
    Study of the Mass in a certain shell
    Input: Radius, Temperature and the Polytrope model constant 
    Output: Value of P(r)
    '''
    return K * T**2.5
#--------------------------------------------------------------------------------------------------------


# We can define a function to calculate the total relative error
def TotalRelEror(P_rad, P_con, T_rad, T_con, L_rad, L_con, M_rad, M_con):
    '''
    Study the total relative error in the frontier between the radioative and convective part
    Inputs: values of pressure, temperature, luminosity and mass in the frontier, in each part
    Output: value of the total relative error
    '''
    
    a = ((P_rad - P_con) / P_rad) ** 2
    b = ((T_rad - T_con) / T_rad) ** 2
    c = ((L_rad - L_con) / L_rad) ** 2
    d = ((M_rad - M_con) / M_rad) ** 2
    return sqrt(a + b + c + d)	






