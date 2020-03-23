
from Parameters_Study import *         # We import all the functions that we have defined
import matplotlib.pyplot as plt        # We import a library for plotting

# We calculate all the parameters for the plotting
parameters_frontier = frontierStudy(1)

Tc = parameters_frontier[0]           # Center temperature that minimaze the relative error
T_prueba1 = parameters_frontier[1]    # Interval of temperatures that we have studied
error_list = parameters_frontier[2]   # Array of relative errors related with the temperatures
pos_min1 = parameters_frontier[3]     # Position of the center temperature that minimaze the relative error


# We create the figure where we will genete the plot
fig, ax = plt.subplots()

# First we will plot the temperatures
ax.plot(T_prueba1, error_list, label = "TRE")                                       # Plotting curve of temperatures
ax.scatter(Tc, error_list[pos_min1], color = (1., 0.5, 0.5), s = 100, label = "Tc") # Plot of the minimum
ax.set_title("Minimal Relative Error", fontsize = 18, fontweight="semibold") # Title
ax.set_xlabel("Center Temperature", fontsize = 13) # X labels
ax.set_ylabel("Relative Error", fontsize = 13)     # Y labels

# Box of text
ax.text(1.75, 0.68, "\nRelative Error = {:.4f} %\n Center Temperature = {:.4f}·10^7 K \n"  
         .format(100 * error_list[pos_min1], Tc), size = 11,
         ha = "center", va = "center",bbox = dict(boxstyle="round",
         ec = (1., 0.5, 0.5), fc = (1., 0.8, 0.8)))

ax.set_xlim(1.6,1.9) # X limits
ax.set_ylim(0,1)     # Y limits
ax.legend(loc='lower left', fontsize = 11) # Plotting the legend
ax.grid()                                  # Plotting the grid

# Finally we show the figure
plt.show()

