
# We are going to define some function that will help us to print the values in a styles way

def helpCreator(X, esp):
    '''
    It helps to generalize the styling of the parameters
    Inputs: the value of the parameter and the number of spaces
    Output: the value with the new style
    '''
    X = "{:.7f}".format(X) # Parameter that we are studying
    return " " * (esp - len(str(X))) + X + " |"

# Using the last function, we will create one that will redifine all the parameters of a shell
def graphCreator(E, f, shell, R, P, T, M, L, n):
    '''
    Stylize all the parameters in one row, that is to say each shell
    Inputs: all the parameters of each shell
    Output: all the parameters stylized
    '''

    global helpCreator

    E = " | " + str(E) + " |"                               # Energy rate production stylized
    f = " " + str(f) + " |"                                 # Phase stylized
    shell = " " * (4 - len(str(shell))) + str(shell) + " |" # Shell stylized 
    R = helpCreator(R, 11)                                  # Radius stylized
    P = helpCreator(P, 11)                                  # Pressure stylized
    T = helpCreator(T, 10)                                  # Temperature stylized
    M = helpCreator(M, 10)                                  # Mass stylized
    L = helpCreator(L, 11)                                  # Luminosity stylized
    n = helpCreator(n, 10)                                  # n-parameter stylized

    # We create the division between two shells
    line = "\n +"+ "-"*4 +"+"+ "-"*8 +"+"+ "-"*5 +"+"+ "-"*12 +"+"+ "-"*12 +"+"+ "-"*11 +"+"+ "-"*11 +"+"+ "-"*12 +"+"+ "-"*11 +"+"
    
    return E + f + shell + R + P + T + M + L + n + line

