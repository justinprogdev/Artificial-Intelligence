

import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
age = ctrl.Antecedent(np.arange(0, 100, 1), 'age')
height = ctrl.Consequent(np.arange(0, 95, 1), 'height')
# fuzzy
age['low'] = fuzz.trimf(age.universe, [2, 4, 8])
height['small'] = fuzz.trimf(height.universe, [15, 30, 35])
age.view()
height.view()
# Define a rule
rule1 = ctrl.Rule(age['low'], height['small'])
control = ctrl.ControlSystem([rule1])
control_simulation = ctrl.ControlSystemSimulation(control)
control_simulation.input['age'] = 5
control_simulation.compute()
height.view(sim=control_simulation)
new_var =0    

