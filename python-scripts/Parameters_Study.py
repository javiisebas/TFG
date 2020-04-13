from numpy import linspace, argmin, full, zeros, where, arange, around
from Model import *


# We will use the parameters values of the minimal relative error, hence we will define a function to do it
def frontierStudy(part):


    # We can print and calculate the relative error for the given center temperature
    print("\nMinimal Relative Error Temperature")
    print("   Tc:   {:.4f}·10⁷K".format(1.5))
    print("   E:    {:.4f} %".format(100*minRelError(1.5, RTot_initial, LTot_initial, False)))

    # Then we can look for the center temperature that minimaze the relative error
    # We generate an interval between two temperatures

    length = 1000                         # Number of division in the interval
    T_prueba1 = linspace(1.5,1.9,length)   # Temperature interval
    # We need to generate an array with the length of the interval to apply the function minRelError over the temperatures
    R_prueba1 = full(length, RTot_initial) # Initial radius
    L_prueba1 = full(length, LTot_initial) # Initial Luminosity
    control_prueba1 = full(length, False)  # Initial control (False)

    # We create an array with all the relative error
    error_list = list(map(minRelError, T_prueba1, R_prueba1, L_prueba1, control_prueba1))
    # Then we look for the position of the minimum value
    pos_min1 = argmin(error_list)

    # We get the center temperature with the minimal relative error
    Tc = T_prueba1[pos_min1] # Calculated center temperature

    # We can print the value of the center temperature with its corresponding relative error
    print("\nMinimal Relative Error Temperature")
    print("   Tc:   {:.4f}·10⁷K".format(Tc))
    print("   E:    {:.4f} %\n".format(100*minRelError(Tc, RTot_initial, LTot_initial, False)))


    # We can also study the total radius and the total luminosity that minimaze the relative erro
    if part == 2: # Part two of the calculations

        # We define the radius and luminosity interval boundaries 
        R_int = [11.2, 11.3]     # Radius interval boundaries
        L_int = [42, 43]         # Luminosity interval boundaries

        length = 20 # Number of divisions of the interval

        R_prueba2 = linspace(R_int[0], R_int[1], length) # Radius interval
        L_prueba2 = linspace(L_int[0], L_int[1], length) # Luminosity interval

        # As this calculation will be a bit longer than the one with the temperature we will print the percentaje of progress
        print("Study of minimal relative error varying Radius and Luminosity")
        print("-Percentage till end-")

        # We define a matrix with the size of the number of division to host the relative error of each pair (L,R)
        error_matrix = zeros([length, length]) # Matrix of relative errors
        for i in range(length): # Rows
            if (100*(i+1)/length) % 20 == 0: # Progress Percentaje
                print("   {}%".format(round(100*(i+1)/length),0))
            for j in range(length): # Columns
                error_matrix[i, j] = minRelError(Tc, R_prueba2[i], L_prueba2[j], False) # We introduce the values in the matrix

        # Finally we can look for the position of the minimum relative error in the matriz
        pos_min = where(error_matrix == error_matrix.min())

        # With the position, knowing that the rows are the Radius and the columns are the Luminosity
        # we get the radius and luminosity with minimum relative error
        R = R_prueba2[pos_min[0][0]] # Calculated Radius
        L = L_prueba2[pos_min[1][0]] # Calculated Luminosity

        # We can print the value of the radius and luminosity with its corresponding relative error
        print("\nMinimal Relative Error Radius and Luminosity")
        print("   R:    {:.4f}·10^10 cm".format(R))
        print("   L:    {:.4f}·10^33 erg s−1".format(L))
        print("   E:    {:.5f} %\n".format(100*error_matrix[pos_min[0], pos_min[1]][0]))

        #minRelError(Tc, R, L, True)
        # Depending if we have gone up to the second part or just the first one, we will return different things
        return Tc, T_prueba1, error_list, pos_min1, L_prueba2, R_prueba2, error_matrix, pos_min, R_int, L_int, R, L

    else: # Part one of the calculations

        return Tc, T_prueba1, error_list, pos_min1

