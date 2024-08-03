# thermal_analysis.py

import numpy as np
import pandas as pd
from scipy.optimize import minimize
from scipy.integrate import odeint
from scipy.stats import norm

class ThermalAnalysis:
    def __init__(self, thermal_data):
        self.thermal_data = thermal_data
        self.temperature_range = [20, 1000]  # Celsius
        self.time_range = [0, 100]  # seconds

    def thermal_model(self, params, t):
        # Define the thermal model using a system of ODEs
        T, Q = params
        dTdt = -Q * T / (self.thermal_data['specific_heat'] * self.thermal_data['density'])
        return dTdt

    def fit_thermal_model(self):
        # Fit the thermal model to the experimental data using least squares
        def objective(params):
            T, Q = params
            t = np.linspace(self.time_range[0], self.time_range[1], 100)
            T_sim = odeint(self.thermal_model, T, t, args=(Q,))
            return np.sum((T_sim - self.thermal_data['temperature']) ** 2)

        initial_guess = [500, 100]  # initial temperature and heat flux
        result = minimize(objective, initial_guess, method="SLSQP")
        return result.x

    def predict_temperature(self, t):
        # Predict the temperature at a given time using the fitted model
        T, Q = self.fit_thermal_model()
        t_sim = np.linspace(self.time_range[0], self.time_range[1], 100)
        T_sim = odeint(self.thermal_model, T, t_sim, args=(Q,))
        return np.interp(t, t_sim, T_sim)

    def uncertainty_analysis(self):
        # Perform an uncertainty analysis using Monte Carlo simulations
        num_samples = 1000
        T_samples = np.zeros((num_samples, len(self.time_range)))
        for i in range(num_samples):
            T, Q = self.fit_thermal_model()
            t_sim = np.linspace(self.time_range[0], self.time_range[1], 100)
            T_sim = odeint(self.thermal_model, T, t_sim, args=(Q,))
            T_samples[i, :] = T_sim

        T_mean = np.mean(T_samples, axis=0)
        T_std = np.std(T_samples, axis=0)
        return T_mean, T_std

# Example usage
thermal_data = pd.DataFrame({
    'time': [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100],
    'temperature': [20, 50, 70, 90, 110, 130, 150, 170, 190, 210, 230],
    'specific_heat': 1000,  # J/kg-K
    'density': 1000  # kg/m^3
})

analysis = ThermalAnalysis(thermal_data)
T_fit = analysis.fit_thermal_model()
T_pred = analysis.predict_temperature(50)
T_mean, T_std = analysis.uncertainty_analysis()

print("Fitted temperature:", T_fit)
print("Predicted temperature at 50 seconds:", T_pred)
print("Mean and standard deviation of temperature:", T_mean, T_std)
