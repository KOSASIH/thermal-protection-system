# tps_simulator.py

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
from tps_simulation import TPSimulation

class TPSSimulator:
    def __init__(self, tps_design, thermal_data):
        self.tps_design = tps_design
        self.thermal_data = thermal_data
        self.simulation = TPSimulation(tps_design, thermal_data)

    def run_simulation(self):
        # Run the TPS simulation
        self.simulation.simulate_tps()
        self.plot_simulation_results()

    def plot_simulation_results(self):
        # Plot the simulation results
        plt.plot(self.simulation.t, self.simulation.T_tps)
        plt.xlabel('Time (s)')
        plt.ylabel('Temperature (°C)')
        plt.title('TPS Simulation Results')
        plt.show()

    def optimize_tps_design(self):
        # Optimize the TPS design using a genetic algorithm
        from scipy.optimize import differential_evolution
        bounds = [(0.01, 0.1), (1000, 2000), (1000, 2000)]  # bounds for thickness, density, and specific heat
        result = differential_evolution(self.simulation.objective_function, bounds)
        self.tps_design = result.x
        print("Optimized TPS design:", self.tps_design)

    def analyze_simulation_results(self):
        # Analyze the simulation results using statistical methods
        from scipy.stats import mean, std
        T_mean = mean(self.simulation.T_tps)
        T_std = std(self.simulation.T_tps)
        print("Mean temperature:", T_mean)
        print("Standard deviation of temperature:", T_std)

# Example usage
tps_design = [0.05, 1500, 1500]  # initial TPS design
thermal_data = pd.DataFrame({
    'time': [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100],
    'temperature': [20, 50, 70, 90, 110, 130, 150, 170, 190, 210, 230],
    'heat_flux': [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000, 1100]
})

simulator = TPSSimulator(tps_design, thermal_data)
simulator.run_simulation()
simulator.optimize_tps_design()
simulator.analyze_simulation_results()
