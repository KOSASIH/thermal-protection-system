# aero_thermal_simulation.py

import numpy as np
from scipy.integrate import odeint

class AeroThermalSimulation:
    def __init__(self, aero_design, thermal_data):
        self.aero_design = aero_design
        self.thermal_data = thermal_data
        self.t = None
        self.T_wall = None

    def aero_thermal_model(self, T_wall, t, Q_wall, thickness, density, specific_heat):
        # Define the aero-thermal model using a system of ODEs
        dTdt_wall = -Q_wall / (density * specific_heat * thickness)
        return dTdt_wall

    def simulate_aero_thermal(self):
        # Simulate the aero-thermal system using the optimized design variables
        thickness, density, specific_heat = self.aero_design
        T_wall0 = self.thermal_data['temperature'][0]
        Q_wall = self.thermal_data['heat_flux']
        t = np.linspace(self.thermal_data['time'].min(), self.thermal_data['time'].max(), 100)
        self.T_wall = odeint(self.aero_thermal_model, T_wall0, t, args=(Q_wall, thickness, density, specific_heat))
        self.t = t

    def objective_function(self, x):
        # Define the objective function for optimization
        thickness, density, specific_heat = x
        self.aero_design = x
        self.simulate_aero_thermal()
        return np.mean(self.T_wall)  # minimize the mean wall temperature

    def compute_heat_transfer_coefficient(self):
        # Compute the heat transfer coefficient
        h = self.T_wall[-1] / (self.thermal_data['temperature'][-1] - self.T_wall[-1])
        return h
