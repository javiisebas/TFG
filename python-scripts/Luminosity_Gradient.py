
from Parameters_Study import *         # We import all the parameters that we have defined
import matplotlib.pyplot as plt        # We import a library for plotting
import matplotlib.gridspec as gridspec # We import some useefull functions for the plotting
from numpy import zeros

# We want to calculate the center temperature, radius and luminosity that minimize the relative erro
parameters_frontier = frontierStudy(2) # We study our parameters in the frotier

# Ones we have it, we extract the parameters that we are going to use
Tc = parameters_frontier[0]    # Center Temperature
Rfin = parameters_frontier[10] # Radius
Lfin = parameters_frontier[11] # Luminosity

R = parameters_frontier[-2]
Rini = 0.9 * R    # Radius that we use to start the model
h = - Rini / layers  # Integration step

ParametersRad = ParametersRadFun(Rfin, Lfin, False)
ParametersConv = ParametersConvFun(Tc, Rfin, Lfin, ParametersRad, False)

n_rad_i = ParametersRad[5]                  # List of n-parameters
pos = len(n_rad_i)-1                        # Position of the frontier

R_rad_i = ParametersRad[0][:pos]            # Radius in the radioactive envelope
L_rad_i = ParametersRad[3][:pos]            # Luminosity in the radioactive envelope

R_conv_i = ParametersConv[0][::-1]          # Radius in the convective core
L_conv_i = ParametersConv[3][::-1]          # Luminosity in the convective core

R_list = R_rad_i + R_conv_i[1:]             # Radius in all the star
L_list = L_rad_i + L_conv_i[1:]             # Luminosity in all the star

L_plot = zeros(len(L_list))
for i in range(len(L_list)-1):
	L_plot[i] = -1 * (L_list[i+1] - L_list[i])

R_norm = [R / max(R_list) for R in R_list]  # Normalize Radius
L_norm = [L / max(L_plot) for L in L_plot]  # Normalize Luminosity

max_pos = where(L_plot == L_plot.max())[0][0]
R_x = R_norm[max_pos]

Lum_created = 100 * L_list[2*(max_pos+1)-(len(L_list)+1)] / max(L_list)
print("The percentage of photon created in the convective core:\n   Photons:   {:.4f} %\n".format(Lum_created))


fig, ax = plt.subplots(figsize = (10,5))

# First we will plot the temperatures
ax.axhline(0, linewidth=1, color = "black")
ax.axvline(0, linewidth=1, color = "black")

ax.plot(R_norm, L_norm, linewidth=4, color = "#F4D03F", label = "Luminosity(r)")
ax.axvline(R_x, linewidth=2, color = (1., 0.5, 0.5))

ax.text(0.65, 0.5, "   \nMax. percentage = {:.2f} %\n   ".format(100 * R_x), size = 15,
         ha = "center", va = "center",bbox = dict(boxstyle="round",
         ec = (1., 0.5, 0.5), fc = (1., 0.8, 0.8)))

ax.set_title("\nLuminosity - Radius", fontsize = 20, fontweight="semibold") # Title
ax.set_xlabel("Normalize Radius of each shell", fontsize = 15) # X labels
ax.set_ylabel("Normalize Luminosity", fontsize = 15)          # Y labels

ax.set_xlim(-0.05,1.05) # X limits
ax.set_ylim(-0.05,1.05) # Y limits
ax.legend(fontsize = 13) # Plotting the legend
ax.set_facecolor("#E5E8E8")
ax.grid() 

# Finally we show the figure
plt.show()

# Running the following function it will print all the parameters in each shell
# minRelError(Tc, Rfin, Lfin, True) # We asign True to the variable control, in order to print the parameters
