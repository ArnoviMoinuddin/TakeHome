import unittest

import numpy as np


from gen_identicon import ImageGenerator

class TestImageGenerator(unittest.TestCase):

    def test_uniqueness(self):
        input_string1 = "John"
        input_string2 = "Jon"
        
        image1 = np.array(ImageGenerator(input_string1).get_image())
        image2 = np.array(ImageGenerator(input_string2).get_image())
        
        self.assertFalse(np.array_equal(image1, image2), "Identicons for different strings should not be the same.")

    def test_repeatability(self):
        input_string1 = "Matt"
        input_string2 = "Matt"
        
        image1 = np.array(ImageGenerator(input_string1).get_image())
        image2 = np.array(ImageGenerator(input_string2).get_image())
        
        self.assertTrue(np.array_equal(image1, image2), "Identicons for same strings should be the same.")

    def test_consistency(self):
        input_string1 = "Matt"
        input_string2 = "maTT"
        
        image1 = np.array(ImageGenerator(input_string1).get_image())
        image2 = np.array(ImageGenerator(input_string2).get_image())
        
        self.assertTrue(np.array_equal(image1, image2), "Identicons for same name should be the same, regardless of case of string")
    
    
    def test_special_char(self):
        input_string1 = "Jack"
        input_string2 = "Jac:()k"
        
        image1 = np.array(ImageGenerator(input_string1).get_image())
        image2 = np.array(ImageGenerator(input_string2).get_image())
        
        self.assertTrue(np.array_equal(image1, image2), "Identicons for same name should be the same, regardless of special characters")


if __name__ == "__main__":
    unittest.main()
