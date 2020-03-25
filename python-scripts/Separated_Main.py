
from Parameters_Study import *         # We import all the parameters that we have defined
import matplotlib.pyplot as plt        # We import a library for plotting
import matplotlib.gridspec as gridspec # We import some useefull functions for the plotting

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


fig = plt.figure(figsize = (12,6))
gs = gridspec.GridSpec(ncols=13, nrows=13)

# First we will plot the temperatures
ax = ["ax1", "ax2", "ax3", "ax4"]
names = ["Pressure", "Temperature", "Luminosity", "Mass"]
plot_list = [P_plot, T_plot, L_plot, M_plot]
colors = ["#3498DB", "#E74C3C", "#F4D03F", "#2ECC71"]
back_colors = ["#D6EAF8", "#FADBD8", "#FCF3CF", "#D5F5E3"]
gs_ax = [gs[:5,:6], gs[8:,:6], gs[:5,7:], gs[8:,7:]]
#back_colors = ["#AED6F1", "#F5B7B1", "#F9E79F", "#ABEBC6"]

for i in range(len(ax)):
    
    # First we will plot the temperatures
    ax[i] = fig.add_subplot(gs_ax[i])

    ax[i].axhline(0, linewidth=1, color = "black")
    ax[i].axvline(0, linewidth=1, color = "black")

    ax[i].set_title("\n" + names[i] + " - Radius", fontsize = 18, fontweight="semibold") # Title
    ax[i].plot(R_plot, plot_list[i], linewidth=2, color = colors[i], label = names[i] + "(r)")
    ax[i].set_xlabel("Normalize Radius of each shell", fontsize = 13) # X labels
    ax[i].set_ylabel("Normalize " + names[i], fontsize = 13)          # Y labels

    ax[i].set_xlim(-0.05,1.05) # X limits
    ax[i].set_ylim(-0.05,1.05) # Y limits
    ax[i].legend(fontsize = 11) # Plotting the legend
    ax[i].set_facecolor(back_colors[i])
    ax[i].grid() 

# Finally we show the figure
plt.show()

# Running the following function it will print all the parameters in each shell
# minRelError(Tc, Rfin, Lfin, True) # We asign True to the variable control, in order to print the parameters
