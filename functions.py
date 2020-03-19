
from numpy import sqrt
from parameters import *

# Here we will define all the usefull functions


#---------------FUNCTIONS TO CALCULATE EPSILON---------------
# We define a function to study if the temperature is inside the interval
def inside(T1,T2,T):
    check = False
    if T >= T1 and T <= T2:
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

def epsilonPP(T):
    global X, rho, interval_PP
    
    T *= 10
    nu = 0
    epsilon1 = 0 
    X1 = X2 = X
    for interval in interval_PP:
        if inside(interval[0], interval[1], T):
            epsilon1 = 10**interval[2]
            nu = interval[3]   
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

def epsilonCNO(T):
    global X, Z, rho, interval_CNO
    
    T *= 10
    nu = 0
    epsilon1 = 0 
    X1 = X
    X2 = Z/3
    for interval in interval_CNO:
        if inside(interval[0], interval[1], T):
            epsilon1 = 10**interval[2]
            nu = interval[3]
    return epsilon1 * X1 * X2 * rho * T ** nu

# Finally the energy rate production will be the biggest between th p-p chain and th CNO cycle

def Epsilon(T):
    return max(epsilonPP(T), epsilonCNO(T))


def Dom_epsilon(T):
    
    epsilon = max(epsilonPP(T), epsilonCNO(T))
    
    if epsilon == 0:
        return "--"
    elif epsilon == epsilonPP(T):
        return "PP"
    else:
        return "CN"

#-------------------------------------------------------------


# We define a function to calculate the relative error

def relError(cal,est):
    
    check = False # Repeat
    maximum = 0.0001
    if abs(cal - est) / cal < maximum:
        check = True # Not repeat     
    return check


#----------------FUNCTIONS FOR PHYICAL PARAMETERS----------------
# We are going to define the functions to calculate the different physical parameters
# First for the radioactive surface

def M_fi_rad(P, T, r):
    global mu
    return 0.01523 * mu * P * r**2 / T


def P_fi_rad(P, T, r, M):
    global mu
    return -1 * 8.084 * mu * P * M / (T * r**2)


def T_fi_rad(P, T, r, L):
    global mu, Z, X
    return -1 * 0.01679 * Z * (1+X) * mu**2 * P**2 * L / (T**8.5 * r**2)


def L_fi_rad(P, T, r):
    global mu, Epsilon
    return 0.01845 * Epsilon(T) * mu**2 * P**2 * r**2 / T**2

# Then we define the functions to calcula the T(r) and P(T)

def Temperature(r):
    global RTot, MTot, mu
    return 1.9022 * mu * MTot * ((1/r) - (1/RTot))

def Pressure(T):
    global mu, Z, X, MTot, LTot
    return 10.645 * T**4.25 * sqrt(MTot/(mu * Z * LTot * (1 + X)))

# Second for the convective core

def M_fi_conv(T, r, K):
    global mu
    return 0.01523 * mu * K * T**1.5 * r**2


def P_fi_conv(T, r, M, K):
    global mu
    return -1 * 8.084 * mu * K * T**1.5 * M / r**2


def T_fi_conv(M, r):
    global mu
    return -1 * 3.234 * mu * M / r**2


def L_fi_conv(T, r, K):
    global mu, Epsilon
    return 0.01845 * Epsilon(T) * mu**2 * K**2 * T**3 * r**2
#------------------------------------------------------------------


#-------------FUNCTIONS FOR ESTIMATED PHYICAL PARAMETERS-----------
# We define:
# Estimated Pressure
def P_est_fun(Pi, fi_P, h):
    fi = fi_P[-1]
    fi_1 = fi_P[-2]
    fi_2 = fi_P[-3]
    return Pi + (h/12) * (23*fi - 16*fi_1 + 5*fi_2)

# Estimated Temperatere
def T_est_fun(Ti, fi_T, h):
    fi = fi_T[-1]
    fi_1 = fi_T[-2]
    return Ti + (h/2) * (3*fi - fi_1)

# Calculated Pressure, Temperature and Mass
def Gen_cal_fun(Xi, fi1_X, fi_X, h):
    fi1 = fi1_X
    fi = fi_X[-1]
    return Xi + (h/2) * (fi1 + fi)

# Calculated Luminosity
def L_cal_fun(Li, fi1_L, fi_L, h):
    fi1 = fi1_L
    fi = fi_L[-1]
    fi_1 = fi_L[-1]
    return Li + (h/12) * (5*fi1 + 8*fi - fi_1)
#-------------------------------------------------------------------


# We are going to define n+1:
def n_fun(T_cal, P_cal, fi1_P, fi1_T):
    return (T_cal * fi1_P) / (P_cal * fi1_T)


# Function that checks if the condition of radioactive surface is valid
def check_n_fun(n):
    
    check = True # It True that doesn't meet the condition
    if n <= 2.5:
        check = False
    return check

# We can define a function to calculate all the interpolations
def interpolation(y0,y1):
    
    n = 2.5
    n0 = 2.500934
    n1 = 2.379468 
    return y0 + ((y1 - y0) / (n1 - n0)) * (n - n0)


#----------------FUNCTIONS FOR PHYICAL PARAMETERS----------------
# We are going to define the equations to obtain the parameters in the convective core
# Mass(r)
def M_conv(r, K, Tc):
    global mu
    return 0.005077 * mu * K * Tc**1.5 * r**3

# Luminosity(r)
def L_conv(r, K, Tc):
    global mu, Epsilon    
    return 0.00615 * Epsilon(Tc) * mu**2 * K**2 * Tc**3 * r**3

# Temperature(r)
def T_conv(r, K, Tc):
    global mu 
    return Tc - (0.008207 * mu**2 * K * Tc**1.5 * r**2)

# Pressure(r)
def P_conv(r, T, K): 
    return K * T**2.5
#-------------------------------------------------------------------


# We can define a function to calculate the total relative error
def TotalRelEror(P_rad, P_con, T_rad, T_con, L_rad, L_con, M_rad, M_con):
    
    a = ((P_rad - P_con) / P_rad) ** 2
    b = ((T_rad - T_con) / T_rad) ** 2
    c = ((L_rad - L_con) / L_rad) ** 2
    d = ((M_rad - M_con) / M_rad) ** 2
    return sqrt(a + b + c + d)	






