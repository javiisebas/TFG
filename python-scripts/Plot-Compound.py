
from Parameters_Study import *         # We import all the functions that we have defined
import matplotlib.pyplot as plt        # We import a library for plotting
import matplotlib.gridspec as gridspec # We import some useefull functions for the plotting

# We calculate all the parameters for the plotting
parameters_frontier = frontierStudy(2)

Tc = parameters_frontier[0]           # Center temperature that minimaze the relative error
T_prueba1 = parameters_frontier[1]    # Interval of temperatures that we have studied
error_list = parameters_frontier[2]   # Array of relative errors related with the temperatures
pos_min1 = parameters_frontier[3]     # Position of the center temperature that minimaze the relative error
L_prueba2 = parameters_frontier[4]    # Interval of luminosity that we have studied
R_prueba2 = parameters_frontier[5]    # Interval of radius that we have studied
error_matrix = parameters_frontier[6] # Matrix of relative errors related with the radius and luminosity
pos_min = parameters_frontier[7]      # Position of the mass and luminosity that minimaze the relative error
R_int = parameters_frontier[8]        # Radius interval boundaries
L_int = parameters_frontier[9]        # Luminosity interval boundaries

length = len(L_prueba2)               # Number of divisions of the radius and luminosity interval


# We create the figure where we will genete the plot
fig = plt.figure(figsize = (12,6))
gs = gridspec.GridSpec(ncols=7, nrows=15)

# First we will plot the temperatures
ax1 = fig.add_subplot(gs[3:14, :3])
ax1.plot(T_prueba1, error_list, label = "RelError(T)")                                    # Plotting curve of temperatures
ax1.scatter(Tc, error_list[pos_min1], color = (1., 0.5, 0.5), s = 100, label = "Tcenter") # Plot of the minimum
ax1.set_title("Minimal Relative Error\n", fontsize = 18, fontweight="semibold") # Title
ax1.set_xlabel("Center Temperature", fontsize = 13) # X labels
ax1.set_ylabel("Relative Error", fontsize = 13)     # Y labels

# Box of text
ax1.text(1.75, 0.70, "\nRelative Error = {:.4f} %\n Center Temperature = {:.4f}·10^7 K \n"  
         .format(100 * error_list[pos_min1], Tc), size = 11,
         ha = "center", va = "center",bbox = dict(boxstyle="round",
         ec = (1., 0.5, 0.5), fc = (1., 0.8, 0.8)))

ax1.set_xlim(1.6,1.9) # X limits
ax1.set_ylim(0,1)     # Y limits
ax1.legend(loc='lower left', fontsize = 11) # Plotting the legend
ax1.grid()                                  # Plotting the grid

# Second we will plot the radius and the luminosity
ax2 = fig.add_subplot(gs[2:, 4:])
im = ax2.imshow(100*error_matrix, origin="lower", cmap="inferno", interpolation="bilinear") # Plot of the heat map
cbar = fig.colorbar(im, ax=ax2,fraction=0.0455, pad=0.04) # Creating a color bar
cbar.set_label('Relative Error', fontsize = 13)           # Adjunting the color bar
ax2.set_title("Minimal Relative Error\n", fontsize = 18, fontweight="semibold") # Title
ax2.set_xlabel("Luminosity", fontsize = 13) # X labels
ax2.set_ylabel("Radius", fontsize = 13)     # Y labels

# Box of text
ax2.text((length-1)/2, 0.70*(length-1), "\nRelative Error = {:.4f} %\n Luminosity = {:.4f}·10^33 erg s^−1 \nRadius = {:.4f}·10^10 cm\n"
         .format(100*error_matrix[pos_min[0], pos_min[1]][0], L_prueba2[pos_min[1][0]], R_prueba2[pos_min[0][0]]), size = 11,
         ha = "center", va = "center",bbox = dict(boxstyle="round",
         ec = (1., 0.5, 0.5), fc = (1., 0.8, 0.8)))

num_ticks = 5 # Number of ticks
ax2.set_xticks(around(linspace(0, length-1, num_ticks)))                         # X number of ticks
ax2.set_xticklabels(around(linspace(L_int[0], L_int[1], num_ticks), decimals=2)) # X ticks labels
ax2.set_yticks(around(linspace(0, length-1, num_ticks)))                         # Y number of ticks
ax2.set_yticklabels(around(linspace(R_int[0], R_int[1], num_ticks), decimals=2)) # Y ticks labels

# We add a super title for both graphs
plt.suptitle("\nSTELLAR PARAMETERS\n", fontsize = 24, fontweight="bold")

# Finally we show the figure
plt.show()

