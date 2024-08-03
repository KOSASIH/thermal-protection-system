# test_and_validation.py

import unittest
import numpy as np
from scipy.stats import norm
from cryo_tps_simulation import CryoTPSSimulation
from material_properties import MaterialProperties

class TestCryoTPSSimulation(unittest.TestCase):
    def setUp(self):
        # Set up a CryoTPSSimulation instance for testing
        self.simulation = CryoTPSSimulation()

    def test_cryo_design_variables(self):
        # Test that the cryo design variables are correctly set
        self.simulation.set_cryo_design_variables(thickness=0.01, density=8960, specific_heat=385)
        self.assertEqual(self.simulation.cryo_design, [0.01, 8960, 385])

    def test_simulate_cryo_tps(self):
        # Test that the cryo TPS simulation runs without errors
        self.simulation.simulate_cryo_tps()
        self.assertIsNotNone(self.simulation.T_cryo)

    def test_compute_cryogenic_performance(self):
        # Test that the cryogenic performance metrics are correctly computed
        COP = self.simulation.compute_cryogenic_performance()
        self.assertGreater(COP, 0)

class TestMaterialProperties(unittest.TestCase):
    def setUp(self):
        # Set up a MaterialProperties instance for testing
        self.material_properties = MaterialProperties("Copper", 386, 385, 8960)

    def test_load_property_data(self):
        # Test that the material property data is correctly loaded
        self.material_properties.load_property_data("copper_properties.csv")
        self.assertIsNotNone(self.material_properties.property_data)

    def test_interpolate_thermal_conductivity(self):
        # Test that the thermal conductivity is correctly interpolated
        temperature = 300  # K
        thermal_conductivity = self.material_properties.interpolate_thermal_conductivity(temperature)
        self.assertGreater(thermal_conductivity, 0)

    def test_optimize_material_properties(self):
        # Test that the material properties are correctly optimized
        def objective_function(x):
            return x[0] ** 2 + x[1] ** 2 + x[2] ** 2

        bounds = [(0, 1000), (0, 1000), (0, 1000)]
        self.material_properties.optimize_material_properties(objective_function, bounds)
        self.assertIsNotNone(self.material_properties.material_properties)

class TestUncertaintyQuantification(unittest.TestCase):
    def test_monte_carlo_simulation(self):
        # Test that the Monte Carlo simulation runs without errors
        num_samples = 1000
        simulation_results = []
        for _ in range(num_samples):
            simulation = CryoTPSSimulation()
            simulation.set_cryo_design_variables(thickness=np.random.uniform(0.005, 0.015), density=np.random.uniform(8000, 9000), specific_heat=np.random.uniform(350, 400))
            simulation.simulate_cryo_tps()
            simulation_results.append(simulation.compute_cryogenic_performance())
        self.assertEqual(len(simulation_results), num_samples)

    def test_sensitivity_analysis(self):
        # Test that the sensitivity analysis runs without errors
        simulation = CryoTPSSimulation()
        sensitivity_results = simulation.perform_sensitivity_analysis()
        self.assertIsNotNone(sensitivity_results)

if __name__ == "__main__":
    unittest.main()
