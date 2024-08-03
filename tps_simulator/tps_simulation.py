# tps_simulation.py

import numpy as np
from scipy.integrate import odeint

class TPSimulation:
    def __init__(self, tps_design, thermal_data):
        self.tps_design = tps_design
        self.thermal_data = thermal_data
        self.t = None
        self.T_tps = None

    def tps_model(self, T_tps, t, Q_tps, thickness, density, specific_heat):
        # Define the TPS model using a system of ODEs
        dTdt_tps = -Q_tps / (density * specific_heat * thickness)
        return dTdt_tps

    def simulate_tps(self):
        # Simulate the TPS using the optimized design variables
        thickness, density, specific_heat = self.tps_design
        T_tps0 = self.thermal_data['temperature'][0]
        Q_tps = self.thermal_data['heat_flux']
        t = np.linspace(self.thermal_data['time'].min(), self.thermal_data['time'].max(), 100)
        self.T_tps = odeint(self.tps_model, T_tps0, t, args=(Q_tps, thickness, density, specific_heat))
        self.t = t

    def objective_function(self, x):
        # Define the objective function for optimization
        thickness, density, specific_heat = x
        self.tps_design = x
        self.simulate_tps()
        return np.mean(self.T_tps)  # minimize the mean temperature
