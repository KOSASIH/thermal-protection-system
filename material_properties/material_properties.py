# material_properties.py

import numpy as np
import pandas as pd
from scipy.interpolate import interp1d
from scipy.optimize import minimize

class MaterialProperties:
    def __init__(self, material_name, thermal_conductivity, specific_heat, density):
        self.material_name = material_name
        self.thermal_conductivity = thermal_conductivity
        self.specific_heat = specific_heat
        self.density = density
        self.temperature_range = None
        self.property_data = None

    def load_property_data(self, file_path):
        # Load material property data from a CSV file
        self.property_data = pd.read_csv(file_path)
        self.temperature_range = (self.property_data['Temperature (K)'].min(), self.property_data['Temperature (K)'].max())

    def interpolate_thermal_conductivity(self, temperature):
        # Interpolate thermal conductivity using a cubic spline
        f = interp1d(self.property_data['Temperature (K)'], self.property_data['Thermal Conductivity (W/m-K)'])
        return f(temperature)

    def interpolate_specific_heat(self, temperature):
        # Interpolate specific heat using a cubic spline
        f = interp1d(self.property_data['Temperature (K)'], self.property_data['Specific Heat (J/kg-K)'])
        return f(temperature)

    def compute_thermal_diffusivity(self, temperature):
        # Compute thermal diffusivity using the thermal conductivity and specific heat
        alpha = self.interpolate_thermal_conductivity(temperature) / (self.density * self.interpolate_specific_heat(temperature))
        return alpha

    def optimize_material_properties(self, objective_function, bounds):
        # Optimize material properties using a minimization algorithm
        result = minimize(objective_function, self.material_properties, method="SLSQP", bounds=bounds)
        self.material_properties = result.x
        print("Optimized material properties:", self.material_properties)

    def plot_material_properties(self):
        # Plot material properties as a function of temperature
        plt.plot(self.property_data['Temperature (K)'], self.property_data['Thermal Conductivity (W/m-K)'])
        plt.xlabel('Temperature (K)')
        plt.ylabel('Thermal Conductivity (W/m-K)')
        plt.title('Thermal Conductivity of ' + self.material_name)
        plt.show()

        plt.plot(self.property_data['Temperature (K)'], self.property_data['Specific Heat (J/kg-K)'])
        plt.xlabel('Temperature (K)')
        plt.ylabel('Specific Heat (J/kg-K)')
        plt.title('Specific Heat of ' + self.material_name)
        plt.show()

# Example usage
material_name = "Copper"
thermal_conductivity = 386  # W/m-K at 20°C
specific_heat = 385  # J/kg-K at 20°C
density = 8960  # kg/m³

material_properties = MaterialProperties(material_name, thermal_conductivity, specific_heat, density)
material_properties.load_property_data("copper_properties.csv")
material_properties.plot_material_properties()
