# thermal_data_visualization.py

import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from thermal_analysis import ThermalAnalysis

class ThermalDataVisualization:
    def __init__(self, thermal_data):
        self.thermal_data = thermal_data

    def plot_temperature_vs_time(self):
        # Plot the temperature vs time data
        plt.plot(self.thermal_data['time'], self.thermal_data['temperature'])
        plt.xlabel('Time (s)')
        plt.ylabel('Temperature (°C)')
        plt.title('Temperature vs Time')
        plt.show()

    def plot_temperature_distribution(self):
        # Plot the temperature distribution using a histogram
        sns.distplot(self.thermal_data['temperature'], kde=True)
        plt.xlabel('Temperature (°C)')
        plt.ylabel('Frequency')
        plt.title('Temperature Distribution')
        plt.show()

    def plot_uncertainty_band(self, T_mean, T_std):
        # Plot the uncertainty band using a shaded region
        t = np.linspace(self.thermal_data['time'].min(), self.thermal_data['time'].max(), 100)
        plt.plot(t, T_mean, label='Mean Temperature')
        plt.fill_between(t, T_mean - T_std, T_mean + T_std, alpha=0.3, label='Uncertainty Band')
        plt.xlabel('Time (s)')
        plt.ylabel('Temperature (°C)')
        plt.title('Uncertainty Band')
        plt.legend()
        plt.show()

    def plot_residuals(self, T_fit, T_data):
        # Plot the residuals between the fitted and experimental data
        plt.plot(T_data, T_fit - T_data, 'o')
        plt.xlabel('Experimental Temperature (°C)')
        plt.ylabel('Residuals (°C)')
        plt.title('Residuals')
        plt.show()

    def plot_comparison(self, T_fit, T_data):
        # Plot a comparison between the fitted and experimental data
        plt.plot(T_data, label='Experimental Data')
        plt.plot(T_fit, label='Fitted Data')
        plt.xlabel('Time (s)')
        plt.ylabel('Temperature (°C)')
        plt.title('Comparison of Fitted and Experimental Data')
        plt.legend()
        plt.show()

# Example usage
thermal_data = pd.DataFrame({
    'time': [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100],
    'temperature': [20, 50, 70, 90, 110, 130, 150, 170, 190, 210, 230]
})

analysis = ThermalAnalysis(thermal_data)
T_fit = analysis.fit_thermal_model()
T_mean, T_std = analysis.uncertainty_analysis()

visualization = ThermalDataVisualization(thermal_data)
visualization.plot_temperature_vs_time()
visualization.plot_temperature_distribution()
visualization.plot_uncertainty_band(T_mean, T_std)
visualization.plot_residuals(T_fit, thermal_data['temperature'])
visualization.plot_comparison(T_fit, thermal_data['temperature'])
