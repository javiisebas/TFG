
from Parameters_Study import *         # We import all the functions that we have defined
import matplotlib.pyplot as plt        # We import a library for plotting

# We calculate all the parameters for the plotting
parameters_frontier = frontierStudy(2)

pos_min1 = parameters_frontier[3]     # Position of the center temperature that minimaze the relative error
L_prueba2 = parameters_frontier[4]    # Interval of luminosity that we have studied
R_prueba2 = parameters_frontier[5]    # Interval of radius that we have studied
error_matrix = parameters_frontier[6] # Matrix of relative errors related with the radius and luminosity
pos_min = parameters_frontier[7]      # Position of the mass and luminosity that minimaze the relative error
R_int = parameters_frontier[8]        # Radius interval boundaries
L_int = parameters_frontier[9]        # Luminosity interval boundaries

length = len(L_prueba2)               # Number of divisions of the radius and luminosity interval


# We create the figure where we will genete the plot
fig, ax = plt.subplots()

# We will plot the radius and the luminosity
im = ax.imshow(100*error_matrix, origin="lower", cmap="inferno", vmin=0, interpolation="bilinear") # Plot of the heat map
cbar = fig.colorbar(im, ax=ax) # Creating a color bar
cbar.set_label('Relative Error', fontsize = 13)           # Adjunting the color bar
ax.set_title("Minimal Relative Error", fontsize = 18, fontweight="semibold") # Title
ax.set_xlabel("Luminosity", fontsize = 13) # X labels
ax.set_ylabel("Radius", fontsize = 13)     # Y labels

# Box of text
ax.text((length-1)/2, 0.68*(length-1), "\nRelative Error = {:.4f} %\n Luminosity = {:.4f}·10^33 erg s^−1 \nRadius = {:.4f}·10^10 cm\n"
         .format(100*error_matrix[pos_min[0], pos_min[1]][0], L_prueba2[pos_min[1][0]], R_prueba2[pos_min[0][0]]), size = 11,
         ha = "center", va = "center",bbox = dict(boxstyle="round",
         ec = (1., 0.5, 0.5), fc = (1., 0.8, 0.8)))

num_ticks = 5 # Number of ticks
ax.set_xticks(around(linspace(0, length-1, num_ticks)))                         # X number of ticks
ax.set_xticklabels(around(linspace(L_int[0], L_int[1], num_ticks), decimals=2)) # X ticks labels
ax.set_yticks(around(linspace(0, length-1, num_ticks)))                         # Y number of ticks
ax.set_yticklabels(around(linspace(R_int[0], R_int[1], num_ticks), decimals=2)) # Y ticks labels

# Finally we show the figure
plt.show()

