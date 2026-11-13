import unittest

from disease_info import build_field_precautions, estimate_yield_forecast


class FieldAgentTests(unittest.TestCase):
    def test_estimate_yield_forecast_for_healthy_crop(self):
        result = estimate_yield_forecast("tomato_healthy", 96)
        self.assertGreaterEqual(result["yield_percent"], 90)
        self.assertLessEqual(result["yield_percent"], 100)
        self.assertGreater(result["estimated_harvest_tons_per_hectare"], 0)

    def test_build_field_precautions_for_disease(self):
        precautions = build_field_precautions("tomato_late_blight", 92)
        self.assertGreaterEqual(len(precautions), 4)
        self.assertTrue(any("water" in step.lower() or "isolate" in step.lower() for step in precautions))


if __name__ == "__main__":
    unittest.main()
