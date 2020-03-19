
from functions import *
from numpy import linspace, argmin
import warnings

warnings.filterwarnings("ignore")



#---------------------------------------------RADIOACTIVE SURFACE---------------------------------------------
# This is the code that will generate the integrational method from the surface to the center of the star

fi_P = []
fi_T = []
fi_M = []
fi_L = []

#-----------------------------------PHASE 1-INICIO-----------------------------------
shell = 0
print(" E" +3*" "+ "fase" +3*" " + "i" +5*" "+ "r" +10*" "
     + "P" +10*" "+ "T" +9*" "+ "L" +10*" "+ "M" +9*" "+ "n+1")
while shell <= 2:

    # First we calculate the most basic parameters to keep up with the calculations
    r = Rini + shell*h
    Ti = Temperature(r)
    Pi = Pressure(Ti)
    Ei = Dom_epsilon(Ti)
    Mi = MTot
    Li = LTot
    
    # At the same time we will stock all f_i for each parameter
    fi_P.append(P_fi_rad(Pi, Ti, r, MTot))
    fi_T.append(T_fi_rad(Pi, Ti, r, LTot))
    fi_M.append(0)
    fi_L.append(0)
    
    print("{}  {}  {}  {:.5f}  {:.7f}  {:.7f}  {:.6f}  {:.6f}"
          .format(Ei, "INICIO", shell, r, Pi, Ti, LTot, MTot))
    shell += 1
#-----------------------------------------------------------------------------------
  


#-----------------------------------PHASE 2-A.1.1----------------------------------- 
check_M = True
while check_M:

    # First we have to calculate the value of the estimated pressure and temperatere
    P_est = P_est_fun(Pi, fi_P, h)
    T_est = T_est_fun(Ti, fi_T, h)
    
    # Now we have the first parameters to start or calculation
    shell = len(fi_P) # Number of shell that we are studying
    r = Rini + shell*h
    
    check_T = False
    while not(check_T):
    
        fi1_P = P_fi_rad(P_est, T_est, r, MTot) # fi_P of the new shell that we are studying
        P_cal = Gen_cal_fun(Pi, fi1_P, fi_P, h) # Pressure in the shell

        check_P = relError(P_cal, P_est) # We have to check the relative error
        while not(check_P): # If it False, the calculation will be repeat, with the conditon -> P_est = P_cal
            P_est = P_cal
            fi1_P = P_fi_rad(P_est, T_est, r, MTot)
            P_cal = Gen_cal_fun(Pi, fi1_P, fi_P, h)
            check_P = relError(P_cal, P_est) # Finally we re-check it, if still False, the loop will run again
        
        fi1_T = T_fi_rad(P_cal, T_est, r, LTot) # fi_T of the new shell that we are studying
        T_cal = Gen_cal_fun(Ti, fi1_T, fi_T, h) # Temperatere in the shell
    
        check_T = relError(T_cal, T_est) # Finally we re-check it, if still False, the loop will run again
        T_est = T_cal
    
    # Knowing T_cal and P_cal, now we can calculate M_cal
    fi1_M = M_fi_rad(P_cal, T_cal, r)
    M_cal = Gen_cal_fun(MTot, fi1_M, fi_M, h)
    check_M = relError(M_cal, MTot)
    
    if check_M:  # We have to create this condition or the last one will be printed
        
        Ei = Dom_epsilon(T_cal)
        print("{}  {}  {}  {:.5f}  {:.7f}  {:.7f}  {:.6f}  {:.6f}"
              .format(Ei,"A.1.1.", shell, r, P_cal, T_cal, LTot, MTot))

        fi_P.append(P_fi_rad(P_cal, T_cal, r, M_cal))
        fi_T.append(T_fi_rad(P_cal, T_cal, r, LTot))
        fi_M.append(M_fi_rad(P_cal, T_cal, r))
        fi_L.append(0)

        Pi = P_cal
        Ti = T_cal
        Mi = M_cal    
#-----------------------------------------------------------------------------------



#-----------------------------------PHASE 3-A.1.2-----------------------------------
check_L = True
while check_L:
    
    P_est = P_est_fun(Pi, fi_P, h) # Estimated Pressure
    T_est = T_est_fun(Ti, fi_T, h) # Estimated Temperature

    shell = len(fi_P)
    r = Rini + shell*h # Radius of the shell

    check_T = False # First of all we have to impose the following condition
    while not(check_T):

        # With this last values we can calculate the calculated mass
        fi1_M = M_fi_rad(P_est, T_est, r)
        M_cal = Gen_cal_fun(Mi, fi1_M, fi_M, h) # Calculated mass

        # Finally we can calculate the calculated pressure and then compare it with the relative error
        fi1_P = P_fi_rad(P_est, T_est, r, M_cal) 
        P_cal = Gen_cal_fun(Pi, fi1_P, fi_P, h)

        check_P = relError(P_cal, P_est) # Checked of the relative error
        while not(check_P):
            P_est = P_cal
            fi1_P = P_fi_rad(P_est, T_est, r, M_cal)
            P_cal = Gen_cal_fun(Pi, fi1_P, fi_P, h)
            check_P = relError(P_cal, P_est)

        # One we have a good P_cal, we can calculate T_cal
        fi1_T = T_fi_rad(P_cal, T_est, r, LTot) 
        T_cal = Gen_cal_fun(Ti, fi1_T, fi_T, h) 

        # Again we have to check if the relative error is lower than what we are looking for
        check_T = relError(T_cal, T_est) 
        T_est = T_cal
    
    # Finally we can calculate the Luminosity in each shell and study the relative error
    fi1_L = L_fi_rad(P_cal, T_cal, r)
    L_cal = L_cal_fun(LTot, fi1_L, fi_L, h)
    check_L = relError(L_cal, LTot)
    
    if check_L:
        Ei = Dom_epsilon(T_cal)
        print("{}  {}  {}  {:.5f}  {:.7f}  {:.7f}  {:.6f}  {:.6f}"
              .format(Ei, "A.1.2.", shell, r, P_cal, T_cal, LTot, M_cal))

        fi_P.append(P_fi_rad(P_cal, T_cal, r, M_cal))
        fi_T.append(T_fi_rad(P_cal, T_cal, r, L_cal))
        fi_M.append(M_fi_rad(P_cal, T_cal, r))
        fi_L.append(L_fi_rad(P_cal, T_cal, r))

        Pi = P_cal
        Ti = T_cal
        Mi = M_cal
        Li = L_cal
#-----------------------------------------------------------------------------------



#-----------------------------------PHASE 4-A.1.3-----------------------------------    
check_n = True
while check_n:
    
    P_est = P_est_fun(Pi, fi_P, h) # Estimated Preassure
    T_est = T_est_fun(Ti, fi_T, h) # Estimated Temperature

    shell = len(fi_P) # Number of shell that we are studying
    r = Rini + shell*h # Radius of the shell

    # Same steps as before but with the difference that we use the Luminosity to calculate the Temperature
    check_T = False 
    while not(check_T):
        
        fi1_M = M_fi_rad(P_est, T_est, r)
        M_cal = Gen_cal_fun(Mi, fi1_M, fi_M, h) 

        fi1_P = P_fi_rad(P_est, T_est, r, M_cal) 
        P_cal = Gen_cal_fun(Pi, fi1_P, fi_P, h)

        check_P = relError(P_cal, P_est)
        while not(check_P):
            P_est = P_cal
            fi1_P = P_fi_rad(P_est, T_est, r, M_cal)
            P_cal = Gen_cal_fun(Pi, fi1_P, fi_P, h)
            check_P = relError(P_cal, P_est)
            
        fi1_L = L_fi_rad(P_cal, T_est, r)
        L_cal = L_cal_fun(Li, fi1_L, fi_L, h)
        
        fi1_T = T_fi_rad(P_cal, T_est, r, L_cal) 
        T_cal = Gen_cal_fun(Ti, fi1_T, fi_T, h) 
    
        check_T = relError(T_cal, T_est) 
        T_est = T_cal
        
    # Finally we have to check if or condition is still valid    
    n = n_fun(T_cal, P_cal, fi1_P, fi1_T)
    check_n = check_n_fun(n)
    
    if check_n:
        
        Ei = Dom_epsilon(T_cal)
        print("{}  {}  {}  {:.5f}  {:.7f}  {:.7f}  {:.6f}  {:.6f}  {:.6f}"
              .format(Ei,"A.1.3.", shell, r, P_cal, T_cal, L_cal, M_cal, n))

        fi_P.append(P_fi_rad(P_cal, T_cal, r, M_cal))
        fi_T.append(T_fi_rad(P_cal, T_cal, r, L_cal))
        fi_M.append(M_fi_rad(P_cal, T_cal, r))
        fi_L.append(L_fi_rad(P_cal, T_cal, r))

        Pi = P_cal
        Ti = T_cal
        Mi = M_cal
        Li = L_cal
#-----------------------------------------------------------------------------------



#----------------------------------PHASE 5-CONVEC-----------------------------------
# We have to calculate the value of K' as it will be constant in all the algorithm        
K = Pi / (Ti)**2.5 
        
while r > 0:

    T_est = T_est_fun(Ti, fi_T, h) # Estimated Temperature

    shell = len(fi_P) # Number of shell that we are studying
    r = Rini + shell*h # Radius of the shell
    
    if r > 0:

        # Same steps as before 
        check_T = False 
        while not(check_T):

            P_est = K * T_est**2.5 # Estimated Preassure through the polytrope equation

            fi1_M = M_fi_rad(P_est, T_est, r)
            M_cal = Gen_cal_fun(Mi, fi1_M, fi_M, h) 

            # In this case we are not calculating P_cal as before
            fi1_T = -3.234 * mu * M_cal / r**2
            T_cal = Gen_cal_fun(Ti, fi1_T, fi_T, h) 

            check_T = relError(T_cal, T_est) 
            T_est = T_cal

        P_cal = K * T_cal**2.5 

        # Knowing P_cal and T_cal we can calculate the Luminosit
        fi1_L = L_fi_rad(P_cal, T_cal, r)
        L_cal = L_cal_fun(Li, fi1_L, fi_L, h)
        
        Ei = Dom_epsilon(T_cal)
        print("{}  {}  {}  {:.5f}  {:.7f}  {:.7f}  {:.6f}  {:.6f}  {:.6f}"
              .format(Ei,"CONVEC", shell, r, P_cal, T_cal, L_cal, M_cal, n))
        
        # The first n+1 that will print is the one that has been calculated in the last code.
        # It corresponde to th i+1 shell, exactly the first that we are studying
        n = 0

        # From this point n+1 will be always 0
        
        fi_P.append(P_fi_rad(P_cal, T_cal, r, M_cal))
        fi_T.append(T_fi_rad(P_cal, T_cal, r, L_cal))
        fi_M.append(M_fi_rad(P_cal, T_cal, r))
        fi_L.append(L_fi_rad(P_cal, T_cal, r))

        Pi = P_cal
        Ti = T_cal
        Mi = M_cal
        Li = L_cal
#-----------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------



#-----------------------------------------------CONVECTIVE CORE-----------------------------------------------
#----------------------------------PHASE 1-CONVEC-----------------------------------
fi_P = []
fi_T = []
fi_M = []
fi_L = []

R_conv_i = []
P_conv_i = []
T_conv_i = []
M_conv_i = []
L_conv_i = []

# First of all will be to define or parameters
R_rad = interpolation(1.96650, 1.86300)
h = Rini / 100
Tc = 2

shell = 0
print("\n E" +3*" "+ "fase" +3*" " + "i" +5*" "+ "r" +10*" "
      + "P" +10*" "+ "T" +9*" "+ "L" +10*" "+ "M")
while shell <= 2:
    # We calculate or parameters in the first three layers
    r = shell*h
    Ti = T_conv(r ,K, Tc)
    Mi = M_conv(r ,K, Tc)
    Li = L_conv(r ,K, Tc)
    Pi = P_conv(r, Ti ,K)
    Ei = Dom_epsilon(Ti)
    
    fi_P.append(P_fi_conv(Ti, r, Mi, K))
    fi_T.append(T_fi_conv(Mi, r))
    fi_M.append(M_fi_conv(Ti, r, K))
    fi_L.append(L_fi_conv(Ti, r, K)) 
    
    R_conv_i.append(r)
    P_conv_i.append(Pi)
    T_conv_i.append(Ti)
    M_conv_i.append(Mi)
    L_conv_i.append(Li)
    
    print("{}  {}  {}  {:.5f}  {:.7f}  {:.7f}  {:.6f}  {:.6f}"
          .format(Ei,"INICIO", shell, r, Pi, Ti, Li, Mi))
    shell += 1
#-----------------------------------------------------------------------------------



#----------------------------------PHASE 2-CONVEC-----------------------------------
while r < R_rad:

    T_est = T_est_fun(Ti, fi_T, h) # Estimated Temperature

    shell = len(fi_M)  #Number of shell that we are studying
    r = shell*h # Radius of the shell
    
    check_T = False 
    while not(check_T):

        P_est = K * T_est**2.5 # Estimated Preassure through the polytrope equation
        
        fi1_M = M_fi_conv(T_est, r, K)
        M_cal = Gen_cal_fun(Mi, fi1_M, fi_M, h) 

        # In this case we are not calculating P_cal as before
        fi1_T = T_fi_conv(M_cal, r)
        T_cal = Gen_cal_fun(Ti, fi1_T, fi_T, h) 

        check_T = relError(T_cal, T_est) 
        T_est = T_cal

    P_cal = K * T_cal**2.5 

    # Knowing P_cal and T_cal we can calculate the Luminosit
    fi1_L = L_fi_conv(T_cal, r, K)
    L_cal = L_cal_fun(Li, fi1_L, fi_L, h)

    Ei = Dom_epsilon(T_cal)
    print("{}  {}  {}  {:.5f}  {:.7f}  {:.7f}  {:.6f}  {:.6f}"
          .format(Ei,"CONVEC", shell, r, P_cal, T_cal, L_cal, M_cal))

    fi_P.append(P_fi_conv(T_cal, r, M_cal, K))
    fi_T.append(T_fi_conv(M_cal, r))
    fi_M.append(M_fi_conv(T_cal, r, K))
    fi_L.append(L_fi_conv(T_cal, r, K)) 

    Pi = P_cal
    Ti = T_cal
    Mi = M_cal
    Li = L_cal
    
    R_conv_i.append(r)
    P_conv_i.append(Pi)
    T_conv_i.append(Ti)
    M_conv_i.append(Mi)
    L_conv_i.append(Li)
#-----------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------



# At this point we can study the Total Relative Error and vary the Temperature to look for the one tha minimazes the error
# Hence we define the following function:
#------------------------------------------TOTAL RELATIVE ERROR STUDY-----------------------------------------
def minRelError(T_center):

    global K

    R_rad = interpolation(1.96650, 1.86300)
    P_rad = interpolation(39.8420132, 42.3165500)
    T_rad = interpolation(1.4562414, 1.4917669)
    L_rad = interpolation(66.582873, 66.097434)
    M_rad = interpolation(0.702943, 0.607118)

    fi_P = []
    fi_T = []
    fi_M = []
    fi_L = []

    R_conv_i = []
    P_conv_i = []
    T_conv_i = []
    M_conv_i = []
    L_conv_i = []

    h = Rini / 100
    Tc = T_center

    shell = 0
    while shell <= 2:
        r = shell*h
        Ti = T_conv(r ,K, Tc)
        Mi = M_conv(r ,K, Tc)
        Li = L_conv(r ,K, Tc)
        Pi = P_conv(r, Ti ,K)
    
        fi_P.append(P_fi_conv(Ti, r, Mi, K))
        fi_T.append(T_fi_conv(Mi, r))
        fi_M.append(M_fi_conv(Ti, r, K))
        fi_L.append(L_fi_conv(Ti, r, K)) 
    
        R_conv_i.append(r)
        P_conv_i.append(Pi)
        T_conv_i.append(Ti)
        M_conv_i.append(Mi)
        L_conv_i.append(Li)
    
        shell += 1

    while r < R_rad:

        T_est = T_est_fun(Ti, fi_T, h) 
        shell = len(fi_M) 
        r = shell*h
    
        check_T = False 
        while not(check_T):

            P_est = K * T_est**2.5        
            fi1_M = M_fi_conv(T_est, r, K)
            M_cal = Gen_cal_fun(Mi, fi1_M, fi_M, h)  
            fi1_T = T_fi_conv(M_cal, r)
            T_cal = Gen_cal_fun(Ti, fi1_T, fi_T, h)
            check_T = relError(T_cal, T_est) 
            T_est = T_cal

        P_cal = K * T_cal**2.5 
        fi1_L = L_fi_conv(T_cal, r, K)
        L_cal = L_cal_fun(Li, fi1_L, fi_L, h)

        fi_P.append(P_fi_conv(T_cal, r, M_cal, K))
        fi_T.append(T_fi_conv(M_cal, r))
        fi_M.append(M_fi_conv(T_cal, r, K))
        fi_L.append(L_fi_conv(T_cal, r, K)) 

        Pi = P_cal
        Ti = T_cal
        Mi = M_cal
        Li = L_cal
    
        R_conv_i.append(r)
        P_conv_i.append(Pi)
        T_conv_i.append(Ti)
        M_conv_i.append(Mi)
        L_conv_i.append(Li)

    R_con = interpolation(R_conv_i[19], R_conv_i[18])
    P_con = interpolation(P_conv_i[19], P_conv_i[18])
    T_con = interpolation(T_conv_i[19], T_conv_i[18])
    L_con = interpolation(L_conv_i[19], L_conv_i[18])
    M_con = interpolation(M_conv_i[19], M_conv_i[18])

    return TotalRelEror(P_rad, P_con, T_rad, T_con, L_rad, L_con, M_rad, M_con)


# We generate an interval between two temperatures and with this values we look for ot minimal error temperature
T_prueba = linspace(1.9,2,100)
error_list = list(map(minRelError, T_prueba))
pos_min = argmin(error_list)

print("\nMinimum Relative Error = {:.4f}%\nMinimum Center Temperature = {:.4f}·10⁷K \n"
         .format(100 * error_list[pos_min], T_prueba[pos_min]))



# We can now plot the relative error
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize = [10,6])

ax.plot(T_prueba, error_list, label = "TRE")
ax.scatter(T_prueba[pos_min], error_list[pos_min], color = (1., 0.5, 0.5), s = 100, label = "Tc")
ax.set_title("\nMinimal Relative Error\n", fontsize = 18)
ax.set_xlabel("Center Temperature", fontsize = 13)
ax.set_ylabel("Relative Error", fontsize = 13)
ax.text(1.942, 0.55, "\nMinimum Relative Error = {:.4f} %\n Minimum Center Temperature = {:.4f}·10⁷ K \n"
         .format(100 * error_list[pos_min], T_prueba[pos_min]), size = 13,
         ha = "center", va = "center",bbox = dict(boxstyle="round",
         ec = (1., 0.5, 0.5), fc = (1., 0.8, 0.8)))
ax.set_xlim(1.9,2)
ax.legend(loc='lower right', fontsize = 11)
ax.grid()
plt.show()
#----------------------------------------------------THE END--------------------------------------------------
