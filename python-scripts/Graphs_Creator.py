
'''
 This library creates function that displays graphs of the studied parameters
'''
import matplotlib.pyplot as plt        # We import a library for plotting
import matplotlib.gridspec as gridspec # We import some useefull functions for the plotting
from Parameters_Study import *         # We import all the parameters that we have studied


def Plot_Separeted_Main():
	'''
	Creates a graph of the parameters along the star in separeted canvas
	'''

	fig = plt.figure(figsize = (12,6)) # Figure of the graph
	gs = gridspec.GridSpec(ncols=13, nrows=13) # Grid of the graph

	# Dictionary that will be usefull to create the graphs
	plot_dic = {
		'P_plot' : {'ax':'ax1', 'name':'Pressure', 'color':'#3498DB', 'back_color':'#D6EAF8', 'gs':gs[:5,:6]},
		'T_plot' : {'ax':'ax2', 'name':'Temperature', 'color':'#E74C3C', 'back_color':'#FADBD8', 'gs':gs[8:,:6]},
		'L_plot' : {'ax':'ax3', 'name':'Luminosity', 'color':'#F4D03F', 'back_color':'#FCF3CF', 'gs':gs[:5,7:]},
		'M_plot' : {'ax':'ax4', 'name':'Mass', 'color':'#2ECC71', 'back_color':'#D5F5E3', 'gs':gs[8:,7:]},
	}

	# To do the graph it will create a canvas of one parameter per loop
	for Parameter in plot_dic.keys(): # Gets the keys of the dictionary
	    
	    data = plot_dic[Parameter] # Data 0f the parameter from the dictionary
	    data['ax'] = fig.add_subplot(data['gs']) # Adds the canvas to the figure

	    data['ax'].axhline(0, linewidth = 1, color = 'black') # Creates a horizontal line on 0
	    data['ax'].axvline(0, linewidth = 1, color = 'black') # Creates a vertical line on 0

	    data['ax'].set_title('\n' + data['name'] + ' - Radius', fontsize = 18, fontweight = 'semibold') # Title

	    # Plots the data on the canvas
	    data['ax'].plot(Layers_Parameters['R_plot'], Layers_Parameters[Parameter], 
	    				linewidth = 3, 
	    				color = data['color'], 
	    				label = data['name'] + '(r)')

	    data['ax'].set_xlabel('Normalized Radius of each shell', fontsize = 13) # Sets the X labels
	    data['ax'].set_ylabel('Normalized ' + data['name'], fontsize = 13)      # Sets the Y labels

	    data['ax'].set_xlim(-0.05,1.05) # Sets the X limits
	    data['ax'].set_ylim(-0.05,1.05) # Sets the Y limits
	    data['ax'].legend(loc='center right', fontsize = 11) # Plots the legend of the graph
	    data['ax'].set_facecolor(data['back_color']) # Sets the canvas background color
	    data['ax'].grid() # Adds the grid to the graph

	# Finally we show the figure
	plt.show()



def Plot_Compound_Main():
	'''
	Creates a graph of the parameters along the star a compund canvas
	'''

	fig, ax = plt.subplots(figsize = (8,5)) # Figure of the graph

	ax.axhline(0, linewidth=1, color = 'black') # Creates a horizontal line on 0
	ax.axvline(0, linewidth=1, color = 'black') # Creates a vertical line on 0

	# Dictionary that will be usefull to create the graphs
	plot_dic = {
		'P_plot' : {'label':'Pressure', 'color':'#3498DB'},
		'T_plot' : {'label':'Temperature', 'color':'#E74C3C'},
		'L_plot' : {'label':'Luminosity', 'color':'#F4D03F'},
		'M_plot' : {'label':'Mass', 'color':'#2ECC71'}
	}

	# To do the graph it will create a canvas of one parameter per loop
	for Parameter in plot_dic.keys(): # Gets the keys of the dictionary

		data = plot_dic[Parameter] # Data 0f the parameter from the dictionary
		# Plots the data on the canvas
		ax.plot(Layers_Parameters['R_plot'], Layers_Parameters[Parameter], 
				linewidth = 3, 
				color = data['color'], 
				label = data['label'] + '(r)')

	ax.set_title('Stellar Parameters', fontsize = 18, fontweight='semibold') # Sets the Title
	ax.set_xlabel('Normalized Radius of each shell', fontsize = 13) # Sets the X labels
	ax.set_ylabel('Normalized Parameters', fontsize = 13)           # Sets the Y labels

	ax.set_xlim(-0.05,1.05) # Sets the X limits
	ax.set_ylim(-0.05,1.05) # Sets the Y limits
	ax.legend(loc='center right', fontsize = 11) # Plots the legend of the graph
	ax.set_facecolor('#E5E8E8') # Sets the canvas background color
	ax.grid() # Adds the grid to the graph

	# Finally we show the figure
	plt.show()



def Plot_Luminosity_Gradient():
	'''
	This functions studies the luminosity gradient and creates a graph of it
	'''

	# First will be to study the Luminosity Gradient
	L_plot_Gradient = zeros(len(L_plot)) # Zeros initial array
	for i in range(len(L_plot)-1): # It will calculate the difference between two layers
		L_plot_Gradient[i] = L_plot[i] - L_plot[i+1] # Adds the difference to the list

	max_pos = where(L_plot_Gradient == L_plot_Gradient.max())[0][0] # Calculates the position of the maximum gradient value
	R_max_pos = R_plot[max_pos] # Gets the position of the correspondent radius

	L_plot_Gradient = [L / max(L_plot_Gradient) for L in L_plot_Gradient] # Normalized Luminosity Gradient
	Lum_created = 100 * L_plot[2*(max_pos+1)-(len(L_plot)+1)] / max(L_plot) # Luminosity created on the convective core

	fig, ax = plt.subplots(figsize = (8,5)) # Figure of the graph

	# First we will plot the temperatures
	ax.axhline(0, linewidth=1, color = 'black') # Creates a horizontal line on the graph
	ax.axvline(0, linewidth=1, color = 'black') # Creates a vertical line on the graph

	# Plots the data on the canvas
	ax.plot(R_plot, L_plot_Gradient, linewidth=3, color = '#F4D03F', label = 'Luminosity(r)')
	ax.axvline(R_max_pos, linewidth=2, color = (1., 0.5, 0.5)) # Creates a vertical line on the graph

	# Box of text
	message = ' \nMax. percentage = {:.2f} %'.format(100 * R_max_pos)
	message += '\n   Photons created in the convective core = {:.4f} %   \n'.format(Lum_created)
	# Adds the box with the message to the canvas
	ax.text(0.60, 0.65, message, size = 11,
	         ha = 'center', va = 'center',bbox = dict(boxstyle='round',
	         ec = (1., 0.5, 0.5), fc = (1., 0.8, 0.8)))

	ax.set_title('\nLuminosity - Radius', fontsize = 18, fontweight='semibold') # Sets the Title
	ax.set_xlabel('Normalized Radius of each shell', fontsize = 13) # Sets the X labels
	ax.set_ylabel('Normalized Luminosity', fontsize = 13)           # Sets the Y labels

	ax.set_xlim(-0.05,1.05) # Sets the X limits
	ax.set_ylim(-0.05,1.05) # Sets the Y limits
	ax.legend(fontsize = 13) # Plots the legend of the graph
	ax.set_facecolor('#E5E8E8') # Sets the canvas background color
	ax.grid() # Adds the grid to the graph

	# Finally we show the figure
	plt.show()



def Temperature_Canvas(fig, gs, kind):
	'''
	The function creates a canvas with the Temperature and its relative error
	'''
	# We will use this function to display a simple and a compound graph
	plot_dic = {
		'compound':gs[3:14, :3], 
		'simple':gs[:,:]
	}

	ax = fig.add_subplot(plot_dic[kind]) # Adds the canvas to the figure
	ax.plot(T_study, error_list, label = 'RelError(T)', linewidth = 3) # Plots the curve of temperatures
	ax.scatter(Tc, error_list[pos_min1], color = (1., 0.5, 0.5), s = 100, label = 'Tcenter') # Plots the minimum
	ax.set_title('Minimal Relative Error\n', fontsize = 18, fontweight='semibold') # Sets the Title
	ax.set_xlabel('Center Temperature', fontsize = 13) # Sets the X labels
	ax.set_ylabel('Relative Error', fontsize = 13)     # Sets the Y labels

	# Box of text
	ax.text(1.75, 0.70, '\nRelative Error = {:.4f} %\n Center Temperature = {:.4f}·10^7 K \n'  
	         .format(100 * error_list[pos_min1], Tc), size = 11,
	         ha = 'center', va = 'center',bbox = dict(boxstyle='round',
	         ec = (1., 0.5, 0.5), fc = (1., 0.8, 0.8)))

	ax.set_xlim(1.6,1.9) # Sets the X limits
	ax.set_ylim(0,1)     # Sets the Y limits
	ax.legend(loc='lower left', fontsize = 11) # Plots the legend of the graph
	ax.grid() # Adds the grid to the graph

	return ax # Returns the canvas



def Radius_Luminosity_Canvas(fig, gs, kind):
	'''
	The function creates a canvas with the Radius-Luminosity and its relative error
	'''
	length = len(L_study) - 1 # Number of divisions of the radius and luminosity interval

	# We will use this function to display a simple and a compound graph
	plot_div = {
		'compound':gs[2:, 4:], 
		'simple':gs[:,:]
	}

	# Adds the canvas to the figure
	ax = fig.add_subplot(plot_div[kind])
	# We will plot the radius and the luminosity
	im = ax.imshow(100*error_matrix, origin='lower', cmap='inferno', interpolation='bilinear') # Plot of the heat map

	# Depending on the kind it will create a different colorbar
	if kind == 'compound':
		cbar = fig.colorbar(im, ax=ax, fraction = 0.0455, pad = 0.04) # Creating a color bar
	else:
		cbar = fig.colorbar(im, ax=ax) # Creating a color bar
	cbar.set_label('Relative Error', fontsize = 13) # Sets the label of the color bar
	ax.set_title('Minimal Relative Error', fontsize = 18, fontweight='semibold') # Sets the Title
	ax.set_xlabel('Luminosity', fontsize = 13) # Sets the Sets the X labels
	ax.set_ylabel('Radius', fontsize = 13)     # Y labels

	# Box of text
	Relative_Error = 100*error_matrix[pos_min2[0], pos_min2[1]][0]
	Luminosity = L_study[pos_min2[1][0]]
	Radius = R_study[pos_min2[0][0]]
	# Introduces the data on the text
	text = ('\nRelative Error = {:.4f} % \nLuminosity = {:.4f}·10^33 erg s^−1 \nRadius = {:.4f}·10^10 cm\n'
	.format(Relative_Error, Luminosity, Radius))
	# Creates the box of text on the canvas
	ax.text(length/2, 0.80*length, text, size = 11,
	         ha = 'center', va = 'center',bbox = dict(boxstyle='round',
	         ec = (1., 0.5, 0.5), fc = (1., 0.8, 0.8)))

	num_ticks = 5 # Number of ticks
	ax.set_xticks(around(linspace(0, length, num_ticks))) # X number of ticks
	ax.set_yticks(around(linspace(0, length, num_ticks))) # Y number of ticks
	ax.set_xticklabels(around(linspace(L_interval[0], L_interval[1], num_ticks), decimals=2)) # X ticks labels
	ax.set_yticklabels(around(linspace(R_interval[0], R_interval[1], num_ticks), decimals=2)) # Y ticks labels

	return ax # Returns the canvas



def Plot_Compound():
	'''
	This function creates the compound graph of the Temperature and the Radius-Luminosity
	'''
	fig = plt.figure(figsize = (12,6)) # Figure of the graph
	gs = gridspec.GridSpec(ncols=7, nrows=15) # Grid of the graph

	# As it uses other functions that creats the canvas, we have to introduce what kind of graph are we doing
	kind ='compound'

	# Then we can create the canvas by calling the functions
	ax1 = Temperature_Canvas(fig, gs, kind) # Canvas of the Temperature - Relative Error
	ax2 = Radius_Luminosity_Canvas(fig, gs, kind)  # Canvas of the Radius - Luminosity - Relative Error

	# We add a super title for both graphs
	plt.suptitle('\nSTELLAR PARAMETERS\n', fontsize = 24, fontweight='bold')
	plt.show()



def Plot_Radius_Luminosity():
	'''
	This function creates the a graph of the Radius-Luminosity
	'''
	fig = plt.figure(figsize = (8,5)) # Figure of the graph
	gs = gridspec.GridSpec(ncols=7, nrows=15) # Grid of the graph

	# As it uses other functions that creats the canvas, we have to introduce what kind of graph are we doing
	kind ='simple'

	# Then we can create the canvas by calling the function
	ax = Radius_Luminosity_Canvas(fig, gs, kind) # Canvas of the Radius - Luminosity - Relative Error
	
	# Finally we show the figure
	plt.show()



def Plot_Temperature():
	'''
	This function creates the a graph of the Temperature 
	'''
	fig = plt.figure(figsize = (8,5)) # Figure of the graph
	gs = gridspec.GridSpec(ncols=7, nrows=15) # Grid of the graph

	# As it uses other functions that creats the canvas, we have to introduce what kind of graph are we doing
	kind ='simple'

	# Then we can create the canvas by calling the function
	ax = Temperature_Canvas(fig, gs, kind) # Canvas of the Temperature - Relative Error

	# Finally we show the figure
	plt.show()