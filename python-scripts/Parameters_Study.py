
'''
 This library studies the parameters on the frontier that minimaze the relative error.
 Afterwards it uses that parameters to study the value of the physic magnitude on each shell
'''
from numpy import linspace, argmin, full, zeros, where, arange, around
from Model import * # We import all the algorithms of the model
import pandas as pd # We import a pandas in case we want to save the data


# We will use the parameters values of the minimal relative error, hence we will define a function to do it
def frontierStudy1(show):


    # We can print and calculate the relative error for the given center temperature
    if show:
        print('\nMinimal Relative Error Temperature')
        print('   Tc:   {:.4f}·10⁷K'.format(1.5))
        print('   E:    {:.4f} %'.format(100*minRelError(1.5, RTot_initial, LTot_initial)))

    # Then we can look for the center temperature that minimaze the relative error
    # We generate an interval between two temperatures

    length = 1000                                            # Number of division in the interval
    T_interval = [1.5, 1.9]                                  # Temperature interval boundaries
    T_study = linspace(T_interval[0], T_interval[1], length) # Temperature interval

    # We need to generate an array with the length of the interval to apply the function minRelError over the temperatures
    R_study = full(length, RTot_initial) # Initial radius
    L_study = full(length, LTot_initial) # Initial Luminosity

    # We create an array with all the relative error
    error_list = list(map(minRelError, T_study, R_study, L_study))
    # Then we look for the position of the minimum value
    pos_min1 = argmin(error_list)

    # We get the center temperature with the minimal relative error
    Tc = T_study[pos_min1] # Calculated center temperature

    # We can print the value of the center temperature with its corresponding relative error
    if show:
        print('\nMinimal Relative Error Temperature')
        print('   Tc:   {:.4f}·10⁷K'.format(Tc))
        print('   E:    {:.4f} %\n'.format(100*minRelError(Tc, RTot_initial, LTot_initial)))

    return Tc, T_study, error_list, pos_min1



def frontierStudy2(show):
    # We can also study the total radius and the total luminosity that minimaze the relative erro

    # First of all will be to calculate the Temperature that minimaze the relative error
    frontierStudy1_parameters = frontierStudy1(show) # Parameters from the frontier study !

    Tc = frontierStudy1_parameters[0]         # Temperature that minimize the relative error
    T_study = frontierStudy1_parameters[1]    # Temperature interval
    error_list = frontierStudy1_parameters[2] # Relative error of each temperature of the interval
    pos_min1 = frontierStudy1_parameters[3]   # Position of the Temperature on the list

    # We define the radius and luminosity interval boundaries 
    R_interval = [11.2, 11.3]     # Radius interval boundaries
    L_interval = [42, 43]         # Luminosity interval boundaries

    length = 20 # Number of divisions of the interval

    R_study = linspace(R_interval[0], R_interval[1], length) # Radius interval
    L_study = linspace(L_interval[0], L_interval[1], length) # Luminosity interval

    # As this calculation will be a bit longer than the one with the temperature we will print the percentaje of progress
    if show:
        print('Study of minimal relative error varying Radius and Luminosity')
        print('-Percentage till end-')

    # We define a matrix with the size of the number of division to host the relative error of each pair (L,R)
    error_matrix = zeros([length, length]) # Matrix of relative errors
    for i in range(length): # Rows

        if (100*(i+1)/length) % 20 == 0 and show: # Progress Percentaje
            print('   {}%'.format(round(100*(i+1)/length),0))

        for j in range(length): # Columns
            error_matrix[i, j] = minRelError(Tc, R_study[i], L_study[j]) # We introduce the values in the matrix

    # Finally we can look for the position of the minimum relative error in the matriz
    pos_min2 = where(error_matrix == error_matrix.min())

    # With the position, knowing that the rows are the Radius and the columns are the Luminosity
    # we get the radius and luminosity with minimum relative error
    R = R_study[pos_min2[0][0]] # Calculated Radius
    L = L_study[pos_min2[1][0]] # Calculated Luminosity

    # We can print the value of the radius and luminosity with its corresponding relative error
    if show:
        print('\nMinimal Relative Error Radius and Luminosity')
        print('   R:    {:.4f}·10^10 cm'.format(R))
        print('   L:    {:.4f}·10^33 erg s−1'.format(L))
        print('   E:    {:.5f} %\n'.format(100*error_matrix[pos_min2[0], pos_min2[1]][0]))

    return Tc, R, L, T_study, R_study, L_study, error_list, error_matrix, pos_min1, pos_min2, R_interval, L_interval



# We want to calculate the center temperature, radius and luminosity that minimize the relative erro
parameters_frontier = frontierStudy2(True) # We study our parameters in the frontier

# Ones we have it, we extract the parameters that minimize the relative error that we are going to use
Tc = parameters_frontier[0]           # Center Temperature
Rfin = parameters_frontier[1]         # Radius
Lfin = parameters_frontier[2]         # Luminosity
T_study = parameters_frontier[3]      # Temperature interval
R_study = parameters_frontier[4]      # Radius interval
L_study = parameters_frontier[5]      # Luminosity interval
error_list = parameters_frontier[6]   # Relative Temperature error list
error_matrix = parameters_frontier[7] # Relative Radius-Luminosity error matrix
pos_min1 = parameters_frontier[8]     # Position of the Temperature on the error list
pos_min2 = parameters_frontier[9]     # Position of the Radius-Luminosity on the error matrix
R_interval = parameters_frontier[10]  # Radius interval boundaries
L_interval = parameters_frontier[11]  # Luminosity interval boundaries


# Then we can study the parameters on each layer of the start
ParametersRadEnvelope = ParametersRadEnvelopeFun(Rfin, Lfin) # Parameters of the radioactive envelope on the 0.1% of the star
ParametersRad = ParametersRadFun(Rfin, Lfin) # Parameters of the radioative envelope on the 0.9% of the start
ParametersConv = ParametersConvFun(Tc, Rfin, Lfin, ParametersRad) # Parametes of the convective core

n_rad_i = ParametersRad[-2] # List of the n-parameters
n_list = ParametersRadEnvelope[-1] + n_rad_i
pos = len(n_rad_i)-1        # Position of the frontier


# We can create a function that will help us to compact the parameters in the star
def Parameter_List(parameter):
    '''
    Gets the parameter that we want to extract and returns a list with the value of the parameterin each layer
    '''
    global ParametersRadEnvelope, ParametersRad, ParametersConv, pos

    # Dictionary of the parameters that we want to collect and the positions on the lists
    parameters_dic = {
        'Radius' : 0,
        'Pressure' : 1,
        'Temperature' : 2,
        'Luminosity': 3,
        'Mass': 4,
        'Energy' : 5,
        'Phase' : 6
    }

    # Poaition of the parameters that we have selected on the lists
    n = parameters_dic[parameter]
    
    return ParametersRadEnvelope[n] + ParametersRad[n][:pos] + ParametersConv[n][::-1][1:] 


# We use the function that e have defined before to create the list of the values of the parameters
R_list = Parameter_List('Radius')      # Radius in all the star
P_list = Parameter_List('Pressure')    # Pressure in all the star
T_list = Parameter_List('Temperature') # Temperature in all the star
L_list = Parameter_List('Luminosity')  # Luminosity in all the star
M_list = Parameter_List('Mass')        # Mass in all the star
E_list = Parameter_List('Energy')      # Energy in all the star
f_list = Parameter_List('Phase')       # Phase in all the star


# To graph the parameters we want to have it normalized 
R_plot = [R / max(R_list) for R in R_list]  # Normalized Radius
P_plot = [P / max(P_list) for P in P_list]  # Normalized Pressure
T_plot = [T / max(T_list) for T in T_list]  # Normalized Temperature
L_plot = [L / max(L_list) for L in L_list]  # Normalized Luminosity
M_plot = [M / max(M_list) for M in M_list]  # Normalized Mass


# Dictionary of the parameters with its name, it will be used on the graphs
Layers_Parameters = {
'R_plot' : R_plot,
'P_plot' : P_plot,
'T_plot' : T_plot,
'L_plot' : L_plot,
'M_plot' : M_plot
}

# In case we want to save the parameters values we can call this function that will create a csv
def Save_Layers_Parameters_Fun(Layers_Parameters):
    '''
    Gets the dictionaty of parameters as inputs
    '''

    # We create the DataFrame and then we save it with the name 'Layers_Parameters.csv'
    df_Parameters = pd.DataFrame(Layers_Parameters)
    df_Parameters.to_csv('Layers_Parameters.csv')