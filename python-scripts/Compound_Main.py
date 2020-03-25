
from Parameters_Study import *    # We import all the parameters that we have defined
import matplotlib.pyplot as plt   # We import a library for plotting

# We want to calculate the center temperature, radius and luminosity that minimize the relative erro
parameters_frontier = frontierStudy(2) # We study our parameters in the frotier

# Ones we have it, we extract the parameters that we are going to use
Tc = parameters_frontier[0]    # Center Temperature
Rfin = parameters_frontier[10] # Radius
Lfin = parameters_frontier[11] # Luminosity

ParametersRad = ParametersRadFun(Rfin, Lfin, True)
ParametersConv = ParametersConvFun(Tc, Rfin, Lfin, ParametersRad, True)

n_rad_i = ParametersRad[5]                  # List of n-parameters
pos = len(n_rad_i)-1                        # Position of the frontier

R_rad_i = ParametersRad[0][:pos]            # Radius in the radioactive envelope
P_rad_i = ParametersRad[1][:pos]            # Pressure in the radioactive envelope
T_rad_i = ParametersRad[2][:pos]            # Temperature in the radioactive envelope
L_rad_i = ParametersRad[3][:pos]            # Luminosity in the radioactive envelope
M_rad_i = ParametersRad[4][:pos]            # Mass in the radioactive envelope

R_conv_i = ParametersConv[0][::-1]          # Radius in the convective core
P_conv_i = ParametersConv[1][::-1]          # Pressure in the convective core
T_conv_i = ParametersConv[2][::-1]          # Temperature in the convective core
L_conv_i = ParametersConv[3][::-1]          # Luminosity in the convective core
M_conv_i = ParametersConv[4][::-1]          # Mass in the convective core

R_list = R_rad_i + R_conv_i                 # Radius in all the star
P_list = P_rad_i + P_conv_i                 # Pressure in all the star
T_list = T_rad_i + T_conv_i                 # Temperature in all the star
L_list = L_rad_i + L_conv_i                 # Luminosity in all the star
M_list = M_rad_i + M_conv_i                 # Mass in all the star

R_plot = [R / max(R_list) for R in R_list]  # Normalize Radius
P_plot = [P / max(P_list) for P in P_list]  # Normalize Pressure
T_plot = [T / max(T_list) for T in T_list]  # Normalize Temperature
L_plot = [L / max(L_list) for L in L_list]  # Normalize Luminosity
M_plot = [M / max(M_list) for M in M_list]  # Normalize Mass

fig, ax = plt.subplots()

# First we will plot the temperatures
ax.axhline(0, linewidth=1, color = "black")
ax.axvline(0, linewidth=1, color = "black")

ax.plot(R_plot, P_plot, linewidth=2, color = "#3498DB", label = "Pressure(R)")
ax.plot(R_plot, T_plot, linewidth=2, color = "#E74C3C", label = "Temperature(R)")
ax.plot(R_plot, L_plot, linewidth=2, color = "#F4D03F", label = "Luminosity(R)")
ax.plot(R_plot, M_plot, linewidth=2, color = "#2ECC71", label = "Mass(R)")

ax.set_title("Stellar Parameters", fontsize = 18, fontweight="semibold") # Title
ax.set_xlabel("Normalize Radius of each shell", fontsize = 13) # X labels
ax.set_ylabel("Normalize Parameters", fontsize = 13)           # Y labels

ax.set_xlim(-0.05,1.05) # X limits
ax.set_ylim(-0.05,1.05) # Y limits
ax.legend(loc='lower rigth', fontsize = 11) # Plotting the legend
ax.set_facecolor("#E5E8E8")
ax.grid() 

# Finally we show the figure
plt.show()

# Running the following function it will print all the parameters in each shell
# minRelError(Tc, Rfin, Lfin, True) # We asign True to the variable control, in order to print the parameters
