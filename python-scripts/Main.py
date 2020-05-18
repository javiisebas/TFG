
'''
 This library create a terminal interface to obtain the graphics and the value of the parameters on each shell
'''
from Graphics_Creator import * # We import all the functions that create the graphics
from Print_Helper import * 



def Print_Data(save):
	'''
	The function uses the a funcion that stylice the data to print them
	'''
	graphCreator(E_list, f_list, R_list, P_list, T_list, M_list, L_list, n_list, save)



def MainRun():
	'''
	This functions will run on a constant loop in case the user wants to exit.
	Asks what graph does the user wants to visualize
	'''

	# First is to define what actions will be able to do the user
	# We define the key and its function that creates a graph
	possible_executions = {
		'1' : Plot_Temperature,
		'2' : Plot_Radius_Luminosity,
		'3' : Plot_Compound,
		'4' : Plot_Compound_Main,
		'5' : Plot_Separeted_Main,
		'6' : Plot_Luminosity_Gradient,
		'7' : Print_Data
	}

	# We define whether or not we want to save the graphics
	save_option = False

	# We create an inforative message that the user will be able to read
	messages = ['\nWelcome to the stellar interior evolution graph display interface.',
			   'To display a graph enter the number of its index, in case you want',
			   'finish the session just type "0" or "exit".\n']

	# Prints the message
	for message in messages:
		print(message)

	# Prints the possible executions
	print('	1. Temperature - Relative Error')
	print('	2. Radius - Luminosity - Relative Error')
	print('	3. Compound 1 and 2')
	print('	4. Parameters - Radius (Compound)')
	print('	5. Parameters - Radius (Separeted)')
	print('	6. Luminosity Gradient - Radius')
	print('	7. Value of the Parameters in each shell\n')

	# Calls the main loop
	run = True
	while run:

		# Asks what graph does the user wants to visualize
		user = input('Introduce the index of the graph you want to visualize: ')

		# In case the user wants to exit the interface
		if user == '0' or user == 'exit':
			run = False

		# In case the user introduces something that is not expected
		elif user not in possible_executions.keys():
			print('\n   Unrecognized code, Try it again\n')

		# In case the user introduces a correct graph index
		else:
			possible_executions[user](save_option)


# Finally we call the function in order to run the interface when this file gets executed
MainRun()