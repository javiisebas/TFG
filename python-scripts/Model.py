
from Defined_Functions import * # We import all the functions that we have defined
import warnings                 # As there some problems with the zero divide, we do not want to get any warning message
from Print_Helper import *      # We import a function to make our printed values more styles

warnings.filterwarnings("ignore")


# We define or initial parameters
RTot_initial = 12  # Initial Radius
LTot_initial = 40  # Initial Luminosity
layers = 100       # We divide or star in 100 layers



def ParametersRadFun(RTot, LTot, control):

    '''
     This function study the stellar parameters in the radioactive enve
     -lope.

     It takes as inputs the total Radius, the total Luminosity and the 
     control parameter, that it will comunicate to the function whether 
     or not we want to get the values of the parameters in each shell.
  
     The model consist in an integrational methon from the surface to
     the center of the star, going through different phases and conside-
     ration.

     The outputs that we get are the values ​​of the physical parameters 
     in the radioactive envelope
    '''

    global layers

    #---------------------------------------------RADIOACTIVE SURFACE---------------------------------------------
    # This is the code that generates the integrational method from the surface to the center of the star

    # First of all we have to define the lists where we will host the parameters
    # Lists that host the fi or each parameter
    fi_P = [] # Pressure fi
    fi_T = [] # Temperature fi
    fi_M = [] # Mass fi
    fi_L = [] # Luminosity fi
  
    # Lists that host the value or each parameter
    R_rad_i = [] # Radius in the radioactive surface
    P_rad_i = [] # Pressure in the radioactive surface
    T_rad_i = [] # Temperature in the radioactive surface
    M_rad_i = [] # Mass in the radioactive surface
    L_rad_i = [] # Luminosity in the radioactive surface
    E_rad_i = [] # Energy rate production in the radioactive surface
    n_rad_i = [] # n-parameter in the radioactive surface
    f_rad_i = [] # phase in the radioative surface

    initial_layers = 10
    h = -0.1 * RTot / initial_layers

    #-----------------------------------PHASE 0-INICIO-----------------------------------
    # We calculate or parameters starting from the total radius, just in case we want to print the parameters
    if control:

        # We wint some lines to make the printed parameters more styles
        print("\nParameters in each shell \n")
        print(4*" "+ "E" +4*" "+ "fase" +5*" " + "i" +9*" "+ "r" +12*" "+ "P" +11*" "+ "T" +11*" "+ "M" +12*" "+ "L" +10*" "+ "n+1")
        print(" +"+ "-"*4 +"+"+ "-"*8 +"+"+ "-"*5 +"+"+ "-"*12 +"+"+ "-"*12 +"+"+ "-"*11 +"+"+ "-"*11 +"+"+ "-"*12 +"+"+ "-"*11 +"+")

        shell = 0
        while shell < initial_layers:

            r = RTot + shell*h        # Radius of each shell
            Ti = T_rad_fun(r, RTot)   # Temperature of each shell
            Pi = P_rad_fun(Ti, LTot)  # Pressure of each shell
            Mi = MTot                 # Mass behind each shell
            Li = LTot                 # Luminosity of each shell
            Ei = Dom_epsilon(Ti)      # Energy rate production in each shell

            shell += 1 # As the loop is running, we have to increase the shell that we are studying
  
            # We want to print the values we will do it in a visual way
            print(graphCreator(Ei, "^^^^^^", shell-11, r, Pi, Ti, Mi, Li, 0))
    #-----------------------------------------------------------------------------------

    Rini = 0.9 * RTot    # Radius that we use to start the model
    h = - Rini / layers  # Integration step

    #-----------------------------------PHASE 1-INICIO-----------------------------------
    # We calculate or parameters in the first three layers
    shell = 0
    while shell <= 2:

        r = Rini + shell*h        # Radius of each shell
        Ti = T_rad_fun(r, RTot)   # Temperature of each shell
        Pi = P_rad_fun(Ti, LTot)  # Pressure of each shell
        Mi = MTot                 # Mass behind each shell
        Li = LTot                 # Luminosity of each shell
        Ei = Dom_epsilon(Ti)      # Energy rate production in each shell

        # Now we calculate fi of each parameters, except fi_M and fi_L as both are zero
        fi_P.append(P_fi_rad(Pi, Ti, r, Mi))
        fi_T.append(T_fi_rad(Pi, Ti, r, Li))
        fi_M.append(0)
        fi_L.append(0)

        # We add the parameters in the list
        R_rad_i.append(r)
        P_rad_i.append(Pi)
        T_rad_i.append(Ti)
        M_rad_i.append(Mi)
        L_rad_i.append(Li)
        E_rad_i.append(Ei)
        n_rad_i.append(0)
        f_rad_i.append("INICIO")

        shell += 1 # As the loop is running, we have to increase the shell that we are studying
    #-----------------------------------------------------------------------------------
  


    #-----------------------------------PHASE 2-A.1.1-----------------------------------
    # We are considering that the mass and the luminosity are constant
    check_M = True # Initial condition of the mass relative error
    while check_M:

        # First we have to calculate the value of the estimated pressure and temperatere
        P_est = P_est_fun(Pi, fi_P, h) # Estimated Pressure
        T_est = T_est_fun(Ti, fi_T, h) # Estimated Temperature

        # Now we have the first parameters to start or calculation
        shell = len(fi_P)   # Number of shell that we are studying
        r = Rini + shell*h  # Radius of the shell

        check_T = False # Initial condition of the temperature relative error
        while not(check_T):

            fi1_P = P_fi_rad(P_est, T_est, r, MTot) # fi_P of the shell that we are studying
            P_cal = Gen_cal_fun(Pi, fi1_P, fi_P, h) # Calculated pressure in the shell

            check_P = relError(P_cal, P_est) # We want to minimaze the relative error of the calculated parameters
            while not(check_P): # If it False, the calculation will be repeat with the following condition
                P_est = P_cal   # Condition 

                # We repeat the last steps
                fi1_P = P_fi_rad(P_est, T_est, r, MTot) # We calculate again fi_p
                P_cal = Gen_cal_fun(Pi, fi1_P, fi_P, h) # And the calculated pressure

                # We will do this process till or relative error is less than 0.0001
                check_P = relError(P_cal, P_est) 

            # Onces we have a good value of the calculated pressure, we can calculate the following parameters:
            fi1_T = T_fi_rad(P_cal, T_est, r, LTot) # fi_T of the shell that we are studying
            T_cal = Gen_cal_fun(Ti, fi1_T, fi_T, h) # Calculated temperature in the shell

            # We do the same process as with the pressure, we want to minimaze the relative error
            check_T = relError(T_cal, T_est) # All the process will be calculated till this is True
            T_est = T_cal

        # Finally we can calculate the mass with a good values of the Pressure and the Temperature
        fi1_M = M_fi_rad(P_cal, T_cal, r)         # fi_M of the shell that we are studying
        M_cal = Gen_cal_fun(MTot, fi1_M, fi_M, h) # Calculated mass in the shell
        check_M = relError(M_cal, MTot)           # We are sutdying whether we can continue to consider the constant mass 

        if check_M: # We will introduce or parameters in the list just if the condition is still valid

            # Now we calculate fi of each parameters with the calculated values, except fi_L that is zero
            fi_P.append(P_fi_rad(P_cal, T_cal, r, M_cal))
            fi_T.append(T_fi_rad(P_cal, T_cal, r, LTot))
            fi_M.append(M_fi_rad(P_cal, T_cal, r))
            fi_L.append(0)

            # We redefine or parameters for the next calculations
            Pi = P_cal
            Ti = T_cal
            Mi = M_cal 
            Ei = Dom_epsilon(Ti)   

            # We add the parameters in the list
            R_rad_i.append(r)
            P_rad_i.append(Pi)
            T_rad_i.append(Ti)
            M_rad_i.append(Mi)
            L_rad_i.append(Li)
            E_rad_i.append(Ei)
            n_rad_i.append(0)
            f_rad_i.append("A.1.1.")
    #-----------------------------------------------------------------------------------
  


    #-----------------------------------PHASE 3-A.1.2----------------------------------- 
    # We are considering that the luminosity is constant
    check_L = True # Initial condition of the luminosity relative error
    while check_L:

        # First we have to calculate the value of the estimated pressure and temperatere
        P_est = P_est_fun(Pi, fi_P, h) # Estimated Pressure
        T_est = T_est_fun(Ti, fi_T, h) # Estimated Temperature
 
        # Now we have the first parameters to start or calculation
        shell = len(fi_P)  # Number of shell that we are studying
        r = Rini + shell*h # Radius of the shell

        check_T = False # Initial condition of the temperature relative error
        while not(check_T):

            # In this case we are going to calculate the mass first, due to we can no longer considere it constant
            fi1_M = M_fi_rad(P_est, T_est, r)        # fi_M of the shell that we are studying
            M_cal = Gen_cal_fun(Mi, fi1_M, fi_M, h)  # Calculated temperature in the shell

            # Now with the calculated mass we can calculate de pressure
            fi1_P = P_fi_rad(P_est, T_est, r, M_cal) # fi_P of the shell that we are studying
            P_cal = Gen_cal_fun(Pi, fi1_P, fi_P, h)  # Calculated pressure in the shell

            # We apply the same process as in the PHASE 2 for the calculated pressure
            check_P = relError(P_cal, P_est) 
            while not(check_P):
                P_est = P_cal

                fi1_P = P_fi_rad(P_est, T_est, r, M_cal)
                P_cal = Gen_cal_fun(Pi, fi1_P, fi_P, h)

                check_P = relError(P_cal, P_est)
            
            # Onces we have a good value of the calculated pressure, we calculate the temperature as in the PHASE 2
            fi1_T = T_fi_rad(P_cal, T_est, r, LTot) 
            T_cal = Gen_cal_fun(Ti, fi1_T, fi_T, h) 

            check_T = relError(T_cal, T_est) 
            T_est = T_cal

        # Finally we can calculate the mass with a good values of the Pressure and the Temperature
        fi1_L = L_fi_rad(P_cal, T_cal, r)       # fi_L of the shell that we are studying
        L_cal = L_cal_fun(LTot, fi1_L, fi_L, h) # Calculated luminosity in the shell
        check_L = relError(L_cal, LTot)         # We are sutdying whether we can continue to consider the constant luminosity

        if check_L: # We will introduce or parameters in the list just if the condition is still valid
 
            # Now we calculate fi of each parameters with the calculated values
            fi_P.append(P_fi_rad(P_cal, T_cal, r, M_cal))
            fi_T.append(T_fi_rad(P_cal, T_cal, r, L_cal))
            fi_M.append(M_fi_rad(P_cal, T_cal, r))
            fi_L.append(L_fi_rad(P_cal, T_cal, r))

            # We redefine or parameters for the next calculations
            Pi = P_cal
            Ti = T_cal
            Mi = M_cal
            Li = L_cal
            Ei = Dom_epsilon(Ti)

            # We add the parameters in the list
            R_rad_i.append(r)
            P_rad_i.append(Pi)
            T_rad_i.append(Ti)
            M_rad_i.append(Mi)
            L_rad_i.append(Li)
            E_rad_i.append(Ei)
            n_rad_i.append(0)
            f_rad_i.append("A.1.2.")
    #-----------------------------------------------------------------------------------
  


    #-----------------------------------PHASE 4-A.1.3----------------------------------- 
    # We are considering that we can still use the radioactive behavior for the calculations
    check_n = True # Initial condition of the n-parameter (n >= 2.5)
    while check_n:

        # First we have to calculate the value of the estimated pressure and temperatere
        P_est = P_est_fun(Pi, fi_P, h) # Estimated Pressure
        T_est = T_est_fun(Ti, fi_T, h) # Estimated Temperature

        # Now we have the first parameters to start or calculation
        shell = len(fi_P)  # Number of shell that we are studying
        r = Rini + shell*h # Radius of the shell 

        check_T = False # Initial condition of the temperature relative error
        while not(check_T):

            fi1_M = M_fi_rad(P_est, T_est, r)        # fi_M of the shell that we are studying
            M_cal = Gen_cal_fun(Mi, fi1_M, fi_M, h)  # Calculated mass in the shell

            fi1_P = P_fi_rad(P_est, T_est, r, M_cal) # fi_P of the shell that we are studying
            P_cal = Gen_cal_fun(Pi, fi1_P, fi_P, h)  # Calculates pressure in the shell

            # We apply the same process as in the PHASE 2 for the calculated pressure
            check_P = relError(P_cal, P_est)
            while not(check_P):
                P_est = P_cal

                fi1_P = P_fi_rad(P_est, T_est, r, M_cal)
                P_cal = Gen_cal_fun(Pi, fi1_P, fi_P, h)

                check_P = relError(P_cal, P_est)
           
            # In this case we are going to calculate the luminosity first, due to we can no longer considere it constant
            fi1_L = L_fi_rad(P_cal, T_est, r)        # fi_L of the shell that we are studying
            L_cal = L_cal_fun(Li, fi1_L, fi_L, h)    # Calculated luminosity in the shell

            # Now with the calculated luminosity we can calculate the temperature
            fi1_T = T_fi_rad(P_cal, T_est, r, L_cal) # fi_T of the shell that we are studying 
            T_cal = Gen_cal_fun(Ti, fi1_T, fi_T, h)  # Calculated temperatere in the shell
   
            # We want to minimaze the relative error
            check_T = relError(T_cal, T_est) 
            T_est = T_cal

        # Finally we can calculate the n-parameter with a good values of the Pressure and the Temperature
        fi1_P = P_fi_rad(P_cal, T_cal, r, M_cal) # We calculate again fi_P in the new shell with our new values
        fi1_T = T_fi_rad(P_cal, T_cal, r, L_cal) # We calculate again fi_T in the new shell with our new values
        n = n_fun(T_cal, P_cal, fi1_P, fi1_T)    # We are studying if the consition is still valid (n>2.5)
        check_n = check_n_fun(n)                 # We are studying whether we can continue to consider the radioactive behavior

        if check_n: # We will introduce or parameters in the list just if the condition is still valid

            # Now we calculate fi of each parameters with the calculated values
            fi_P.append(P_fi_rad(P_cal, T_cal, r, M_cal))
            fi_T.append(T_fi_rad(P_cal, T_cal, r, L_cal))
            fi_M.append(M_fi_rad(P_cal, T_cal, r))
            fi_L.append(L_fi_rad(P_cal, T_cal, r))

            # We redefine or parameters for the next calculations
            Pi = P_cal
            Ti = T_cal
            Mi = M_cal
            Li = L_cal
            Ei = Dom_epsilon(Ti)

            # We add the parameters in the list
            R_rad_i.append(r)
            P_rad_i.append(Pi)
            T_rad_i.append(Ti)
            M_rad_i.append(Mi)
            L_rad_i.append(Li)
            E_rad_i.append(Ei)
            n_rad_i.append(n)
            f_rad_i.append("A.1.3.")
    #-----------------------------------------------------------------------------------

    # We have to calculate the value of K' as it will be constant in all the algorithm
    K = P_cal / (T_cal)**2.5 # Polytrope model constant
    # We will no longer add the n-parameter to the list, but we add the last calculated as is the first of the convective phase
    n_rad_i.append(n)

    #-----------------------------------PHASE 5-CONVEC-----------------------------------
    # We are considering now a convective behavior
    while r > 0: # We will calculate till we get to the center of the star

        # In this case we are just calculating the estimated temperature, due to the pressure will be done with the polytrope
        T_est = T_est_fun(Ti, fi_T, h) # Estimated Pressure

        # Now we have the first parameters to start or calculation
        shell = len(fi_P)  # Number of shell that we are studying
        r = Rini + shell*h # Radius of the shel

        if r > 0: # We will only the calculations if the radius is bigger than zero

            check_T = False # Initial condition of the temperature relative error 
            while not(check_T):

                # We use the polytrope model to calculate the estimated pressure
                P_est = K * T_est**2.5 # Estimated Pressure

                fi1_M = M_fi_rad(P_est, T_est, r)       # fi_M of the shell that we are studying 
                M_cal = Gen_cal_fun(Mi, fi1_M, fi_M, h) # Calculated mass in the shell

                # With the calculated mass we use the convective formulas to calculate the temperature
                fi1_T = -3.234 * mu * M_cal / r**2      # fi_T of the shell that we are studying
                T_cal = Gen_cal_fun(Ti, fi1_T, fi_T, h) # Calculated temperature in the shell 

                # We want to minimaze the relative error
                check_T = relError(T_cal, T_est) 
                T_est = T_cal

            # We use again the polytrope model for the calculated pressure, ones we have a good calculated pressure
            P_cal = K * T_cal**2.5 # Calculated pressure

            # Finally we can calculate the mass with a good values of the Pressure and the Temperature 
            fi1_L = L_fi_rad(P_cal, T_cal, r)     # fi_L of the shell that we are studying
            L_cal = L_cal_fun(Li, fi1_L, fi_L, h) # Calculated luminosity in the shell

            # Now we calculate fi of each parameters with the calculated values
            fi_P.append(P_fi_rad(P_cal, T_cal, r, M_cal))
            fi_T.append(T_fi_rad(P_cal, T_cal, r, L_cal))
            fi_M.append(M_fi_rad(P_cal, T_cal, r))
            fi_L.append(L_fi_rad(P_cal, T_cal, r))

            # We redefine or parameters for the next calculations
            Pi = P_cal
            Ti = T_cal
            Mi = M_cal
            Li = L_cal
            Ei = Dom_epsilon(Ti)

            # We add the parameters in the list
            R_rad_i.append(r)
            P_rad_i.append(Pi)
            T_rad_i.append(Ti)
            M_rad_i.append(Mi)
            L_rad_i.append(Li)  
    #-----------------------------------------------------------------------------------
    #-------------------------------------------------------------------------------------------------------------

    # At this point we have studied all the parameters from the surface to the center of the star
    # If we want to get the values of the parameters, we will define control as True
    pos = len(n_rad_i)-1 # Number of the last radioavtive shell
    if control: 
        # In case we want to print the values we will do it in a visual way
        for i in range(pos): # Just the one that are inside the radioactive part
            print(graphCreator(E_rad_i[i], f_rad_i[i], i, R_rad_i[i], P_rad_i[i], T_rad_i[i], M_rad_i[i], L_rad_i[i], n_rad_i[i]))

    return R_rad_i, P_rad_i, T_rad_i, L_rad_i, M_rad_i, n_rad_i, K



# We apply the model for the initial parameters that we have defined at the beging of the script
# We will use it to study the center temperature that miniaze the relative error, due to we will use the same values 
ParametersRad = ParametersRadFun(RTot_initial, LTot_initial, False)



def ParametersConvFun(Tc, RTot, LTot, ParametersRad, control):

    ''' 
     This function study the stellar parameters in the convective core

     It takes as inputs the total Radius, the total Luminosity, the cen-
     ter Temperature, the parameters in the radioactie envelope and the 
     control parameter, that it will comunicate to the function whether
     or not we want to get the values of the parameters in each shell.
  
     The model consist in an integrational methon from the center to the
     surface of the star, going through different phases and conside-
     ration.

     The outputs that we get are the values ​​of the physical parameters 
     in the radioactive envelope
    '''

    global RTot_initial, LTot_initial, layers


    R_rad_i = ParametersRad[0]  # Radius list in the radioactive part
    n_rad_i = ParametersRad[5]  # List of n-parameters
    K = ParametersRad[  6]      # Polytrope model constant

    # We can calculate the values ​​of the physical parameters in the transition between the radiative and convective regions of the star
    # We will use them to study the relative error of all the model, with tha values obtained integrating from the center
    pos = len(n_rad_i)-1
    R_rad = interpolation(R_rad_i[pos], R_rad_i[pos-1], n_rad_i[-1], n_rad_i[-2])


    #-----------------------------------------------CONVECTIVE CORE-----------------------------------------------
    # Integrational method from the center to the surface of the star

    # First of all we have to define the lists where we will host the parameters
    # Lists that host the fi or each parameter
    fi_P = [] # Pressure fi
    fi_T = [] # Temperature fi
    fi_M = [] # Mass fi
    fi_L = [] # Luminosity fi

    # Lists that host the value or each parameter
    R_conv_i = [] # Radius in the convective core
    P_conv_i = [] # Pressure in the convective core
    T_conv_i = [] # Temperature in the convective core
    M_conv_i = [] # Mass in the convective core
    L_conv_i = [] # Luminosity in the convective core
    E_conv_i = [] # Energy rate production in the convective core

    Rini = 0.9 * RTot  # Radius that we use to start the model
    h = Rini / layers  # Integration step

    #----------------------------------PHASE 1-CONVEC-----------------------------------
    # We calculate or parameters in the first three layers
    shell = 0
    while shell <= 2:
        r = shell*h           # Radius of each shell
        Ti = T_conv(r ,K, Tc) # Temperature of each shell
        Mi = M_conv(r ,K, Tc) # Mass of each shell
        Li = L_conv(r ,K, Tc) # Luminosity of each shell
        Pi = P_conv(r, Ti ,K) # Pressure of each shell
        Ei = Dom_epsilon(Ti)  # Energy rate production in each shell
    
        # Now we calculate fi of each parameters with the calculated values
        fi_P.append(P_fi_conv(Ti, r, Mi, K))
        fi_T.append(T_fi_conv(Mi, r))
        fi_M.append(M_fi_conv(Ti, r, K))
        fi_L.append(L_fi_conv(Ti, r, K)) 
    
        # We add the parameters in the list
        R_conv_i.append(r)
        P_conv_i.append(Pi)
        T_conv_i.append(Ti)
        M_conv_i.append(Mi)
        L_conv_i.append(Li)
        E_conv_i.append(Ei)
    
        shell += 1 # As the loop is running, we have to increase the shell that we are studying
    #-----------------------------------------------------------------------------------



    #----------------------------------PHASE 2-CONVEC-----------------------------------
    # We are using the same structure as the last phase of the integrational model from the surface to the center
    while r < R_rad: # We will calculate till we get to the radius in the frontier

        # First we have to calculate the value of the estimated temperatere
        T_est = T_est_fun(Ti, fi_T, h) # Estimated temperature

        # Now we have the first parameters to start or calculation
        shell = len(fi_M)  # Number of shell that we are studying
        r = shell*h # Radius of the shel
    
        check_T = False # Initial condition of the temperature relative error 
        while not(check_T):

            # We use the polytrope model to calculate the estimated pressure
            P_est = K * T_est**2.5 # Estimated Pressure

            fi1_M = M_fi_conv(T_est, r, K)          # fi_M of the shell that we are studying 
            M_cal = Gen_cal_fun(Mi, fi1_M, fi_M, h) # Calculated mass in the shell

            # With the calculated mass we use the convective formulas to calculate the temperature
            fi1_T = T_fi_conv(M_cal, r)             # fi_T of the shell that we are studying
            T_cal = Gen_cal_fun(Ti, fi1_T, fi_T, h) # Calculated temperature in the shell 

            # We want to minimaze the relative error
            check_T = relError(T_cal, T_est) 
            T_est = T_cal

        # We use again the polytrope model for the calculated pressure, ones we have a good calculated pressure
        P_cal = K * T_cal**2.5 # Calculated pressure

        # Finally we can calculate the mass with a good values of the Pressure and the Temperature 
        fi1_L = L_fi_conv(T_cal, r, K)        # fi_L of the shell that we are studying
        L_cal = L_cal_fun(Li, fi1_L, fi_L, h) # Calculated luminosity in the shell

        # Now we calculate fi of each parameters with the calculated values
        fi_P.append(P_fi_conv(T_cal, r, M_cal, K))
        fi_T.append(T_fi_conv(M_cal, r))
        fi_M.append(M_fi_conv(T_cal, r, K))
        fi_L.append(L_fi_conv(T_cal, r, K)) 

        # We redefine or parameters for the next calculations
        Pi = P_cal
        Ti = T_cal
        Mi = M_cal
        Li = L_cal
    
        # We add the parameters in the list
        R_conv_i.append(r)
        P_conv_i.append(Pi)
        T_conv_i.append(Ti)
        M_conv_i.append(Mi)
        L_conv_i.append(Li)
        E_conv_i.append(Ei)
    #-----------------------------------------------------------------------------------
    #-------------------------------------------------------------------------------------------------------------   

    # At this point we have studied all the parameters from the center to the frontier of the star
    # If we want to get the values of the parameters, we will define control as True
    if control: 
        # In case we want to print the values we will do it in a visual way
        n = n_rad_i[-1] # We want to print the last calculated value of as it is the firt one of the convective part
        for i in range(len(R_conv_i)-1):  # Just the one that are inside the convective part
            print(graphCreator(E_conv_i[i], "CONVEC", pos+i, R_conv_i[-i-2], P_conv_i[-i-2], T_conv_i[-i-2]
                        , M_conv_i[-i-2], L_conv_i[-i-2], n))
            n = 0 # From this point n will be zero

    return R_conv_i, P_conv_i, T_conv_i, L_conv_i, M_conv_i



def minRelError(Tc, RTot, LTot, control):

    ''' 
     This function study the total relative error in the frontier

     It takes as inputs the total Radius, the total Luminosity, the cen-
     ter Temperature and the control parameter, that it will comunicate 
     to the function whether or not we want to get the values of the pa-
     rameters in each shell.

     The outputs that we get is the total relative error
    '''

    global ParametersRad, ParameterRadFun, ParametersConvFun

    # If the total radius or the total luminosity are different than the initial values we have to calculate the parameters again
    # as the ones that we have calculated right before this function, are with the initial values of radius and luminosity
    if RTot != RTot_initial or LTot != LTot_initial:
        ParametersRad = ParametersRadFun(RTot, LTot, control) # New frontier values

    ParametersConv = ParametersConvFun(Tc, RTot, LTot, ParametersRad, control)

    R_rad_i = ParametersRad[0]    # Radius in the radioactive envelope
    P_rad_i = ParametersRad[1]    # Pressure in the radioactive envelope
    T_rad_i = ParametersRad[2]    # Temperature in the radioactive envelope
    L_rad_i = ParametersRad[3]    # Luminosity in the radioactive envelope
    M_rad_i = ParametersRad[4]    # Mass in the radioactive envelope
    n_rad_i = ParametersRad[5]    # List of n-parameters

    R_conv_i = ParametersConv[0]  # Radius in the convective core
    P_conv_i = ParametersConv[1]  # Pressure in the convective core
    T_conv_i = ParametersConv[2]  # Temperature in the convective core
    L_conv_i = ParametersConv[3]  # Luminosity in the convective core
    M_conv_i = ParametersConv[4]  # Mass in the convective core

    # Position of the frontier
    pos = len(n_rad_i)-1

    # We can calculate the values ​​of the physical parameters in the transition between the radiative and convective regions of the star
    # Interpolated values integrating from the surface to the center
    R_rad = interpolation(R_rad_i[pos], R_rad_i[pos-1], n_rad_i[-1], n_rad_i[-2])
    P_rad = interpolation(P_rad_i[pos], P_rad_i[pos-1], n_rad_i[-1], n_rad_i[-2])
    T_rad = interpolation(T_rad_i[pos], T_rad_i[pos-1], n_rad_i[-1], n_rad_i[-2])
    L_rad = interpolation(L_rad_i[pos], L_rad_i[pos-1], n_rad_i[-1], n_rad_i[-2])
    M_rad = interpolation(M_rad_i[pos], M_rad_i[pos-1], n_rad_i[-1], n_rad_i[-2])

    # Interpolated values integrating from the center to the surface
    R_con = interpolation(R_conv_i[layers-pos], R_conv_i[layers+1-pos], n_rad_i[-1], n_rad_i[-2])
    P_con = interpolation(P_conv_i[layers-pos], P_conv_i[layers+1-pos], n_rad_i[-1], n_rad_i[-2])
    T_con = interpolation(T_conv_i[layers-pos], T_conv_i[layers+1-pos], n_rad_i[-1], n_rad_i[-2])
    L_con = interpolation(L_conv_i[layers-pos], L_conv_i[layers+1-pos], n_rad_i[-1], n_rad_i[-2])
    M_con = interpolation(M_conv_i[layers-pos], M_conv_i[layers+1-pos], n_rad_i[-1], n_rad_i[-2])

    return TotalRelEror(P_rad, P_con, T_rad, T_con, L_rad, L_con, M_rad, M_con) # Total relative error in the frontier


