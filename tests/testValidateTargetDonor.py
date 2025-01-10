import unittest
from helper.functionsValidateTarget import validate_target_donor

class TestValidateTargetDonor(unittest.TestCase):
    def setUp(self):
        print("\nStarting a new test case for validate_target_donor...")

    def tearDown(self):
        print("Test case finished\n")

    def test_positive_target(self):
        # Target donor positif harus diterima tanpa error
        self.assertEqual(validate_target_donor(50), 50)

    def test_zero_target(self):
        # Target donor nol harus diterima tanpa error
        self.assertEqual(validate_target_donor(0), 0)

    def test_negative_target(self):
        # Target donor negatif harus memunculkan ValueError
        with self.assertRaises(ValueError):
            validate_target_donor(-10)

if __name__ == '__main__':
    unittest.main(verbosity=2)
