import unittest
from waypoint_core.distance import Distance


class DistanceDomainRuleTests(unittest.TestCase):
    def test_negative_magnitude_rejected(self):
        with self.assertRaises(ValueError):
            Distance(-5, "km")

    def test_addition_operator_overload(self):
        result = Distance(3, "km") + Distance(2, "km")
        self.assertEqual(result, Distance(5, "km"))


if __name__ == "__main__":
    unittest.main()
