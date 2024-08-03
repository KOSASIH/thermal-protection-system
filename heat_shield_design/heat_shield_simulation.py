# heat_shield_simulation.py

import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt

class HeatShieldSimulation:
    def __init__(self, heat_shield_design, thermal_data):
        self.heat_shield_design = heat_shield_design
        self.thermal_data = thermal_data

    def heat_shield_model(self, T_hs, t, Q_hs, density, specific_heat):
        # Define the heat shield model using a system of ODEs
        dTdt_hs = -Q_hs / (density * specific_heat)
        return dTdt_hs

    def simulate_heat_shield(self):
        # Simulate the heat shield using the optimized design variables
        thickness, density, specific_heat = self.heat_shield_design
        T_hs0 = self.thermal_data['temperature'][0]
        Q_hs = self.thermal_data['heat_flux']
        t = np.linspace(self.thermal_data['time'].min(), self.thermal_data['time'].max(), 100)
        T_hs = odeint(self.heat_shield_model, T_hs0, t, args=(Q_hs, density, specific_heat))
        return t, T_hs

    def plot_simulation_results(self, t, T_hs):
        # Plot the simulation results
        plt.plot(t, T_hs)
        plt.xlabel('Time (s)')
        plt.ylabel('Temperature (°C)')
        plt.title('Heat Shield Simulation Results')
        plt.show()

# Example usage
heat_shield_design = [0.05, 1000, 1000]  # optimized design variables
thermal_data = pd.DataFrame({
    'time': [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100],
    'temperature': [20, 50, 70, 90, 110, 130, 150, 170, 190, 210, 230],
    'heat_flux': [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000, 1100]
})

simulation = HeatShieldSimulation(heat_shield_design, thermal_data)
t, T_hs = simulation.simulate_heat_shield()
simulation.plot_simulation_results(t, T_hs)
