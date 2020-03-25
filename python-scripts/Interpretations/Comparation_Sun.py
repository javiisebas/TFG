from Final_Model_Parameters import *

L_Sun = 3.826 * 10**33  # 1 Solar Luminosity [ergs/s]
M_Sun = 1.9891 * 10**33 # 1 Solar Mass [g]
T_Sun = 1.571 * 10**7   # Central temperature [K]
R_Sun = 6.96 * 10**10   # 1 Solor Radius [cm]

print("{}·L Solar Units".format(round(L_Model/L_Sun, 3)))
print("{}·M Solar Units".format(round(M_Model/M_Sun, 4)))
print("{}·T Solar Units".format(round(T_Model/T_Sun, 4)))
print("{}·R Solar Units".format(round(R_Model/R_Sun, 4)))
