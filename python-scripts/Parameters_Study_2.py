from numpy import linspace, argmin, full, zeros, where, arange, around
from Model import *


length = 100                       
T_prueba1 = linspace(1.5,1.9,length)   # Temperature interval
R_prueba1 = full(length, RTot_initial) # Initial radius
L_prueba1 = full(length, LTot_initial) # Initial Luminosity
control_prueba1 = full(length, False)  # Initial control (False)


error_list = list(map(minRelError, T_prueba1, R_prueba1, L_prueba1, control_prueba1))
pos_min1 = argmin(error_list)
Tc = T_prueba1[pos_min1] 



R_int = [11.7, 11.8]     # Radius interval boundaries
L_int = [35, 36]         # Luminosity interval boundaries

length = 10 # Number of divisions of the interval

R_prueba2 = linspace(R_int[0], R_int[1], length) # Radius interval
L_prueba2 = linspace(L_int[0], L_int[1], length) # Luminosity interval


def repeticion(Tc_lista, R_lista, L_lista):
    length = 10
    error_matrix = zeros([length, length])
    for i in range(length): 
        for j in range(length):
            error_matrix[i,j] = []


'''
    for i in range(length): 
        for j in range(length): 
            for k in range(length):
                error_matrix[i, j] = minRelError(Tc_lista[i], R_lista[j], L_lista[k], False) 


    pos_min = where(error_matrix == error_matrix.min())
    R = R_prueba2[pos_min[0][0]] 
    L = L_prueba2[pos_min[1][0]] 

'''


