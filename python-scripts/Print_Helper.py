
# We are going to define some function that will help us to print the values in a styles way

def helpCreator(X, esp):
    '''
    It helps to generalize the styling of the parameters
    Inputs: the value of the parameter and the number of spaces
    Output: the value with the new style
    '''
    X = '{:.7f}'.format(X) # Parameter that we are studying
    return ' ' * (esp - len(str(X))) + X + ' |'
    

# Using the last function, we will create one that will redifine all the parameters of a shell
def graphCreator(E_list, f_list, R_list, P_list, T_list, M_list, L_list, n_list):
    '''
    Stylize all the parameters in one row, that is to say each shell
    Inputs: all the parameters of each shell
    Output: all the parameters stylized
    '''

    global helpCreator

    # We create the division between two shells
    line = '\n +'+ '-'*4 +'+'+ '-'*8 +'+'+ '-'*5 +'+'+ '-'*12 +'+'+ '-'*12 +'+'+ '-'*11 +'+'+ '-'*11 +'+'+ '-'*12 +'+'+ '-'*11 +'+'
    print(line)

    initial_parameter_length = 10    # Number of shells calculated in the radioactive envelope
    length_n_list =  len(n_list) - 1 # Length of the n parameter

    for position in range(len(R_list)):

        E = E_list[position] # Energy of a certain shell
        f = f_list[position] # Phase of a certain shell
        shell = position - initial_parameter_length # Shell
        R = R_list[position] # Radius of a certain shell
        P = P_list[position] # Pressure of a certain shell
        T = T_list[position] # Temperature of a certain shell
        M = M_list[position] # Mass of a certain shell
        L = L_list[position] # Luminosity of a certain shell

        if position > length_n_list: # If the position is bigger than the length of the n parameters list
            n = 0
        else: # In case is not bigger
            n = n_list[position]


        E_print = ' | ' + str(E) + ' |' # Energy rate production stylized
        f_print = ' ' + str(f) + ' |'   # Phase stylized
        shell_print = ' ' * (4 - len(str(shell))) + str(shell) + ' |' # Shell stylized 
        R_print = helpCreator(R, 11)    # Radius stylized
        P_print = helpCreator(P, 11)    # Pressure stylized
        T_print = helpCreator(T, 10)    # Temperature stylized
        M_print = helpCreator(M, 10)    # Mass stylized
        L_print = helpCreator(L, 11)    # Luminosity stylized
        n_print = helpCreator(n, 10)    # n-parameter stylized
    
        # Prints the values stylized
        print(E_print + f_print + shell_print + R_print + P_print + T_print + M_print + L_print + n_print + line)

    print('\n')

