# ------------------------------------------
# | Automated Application Labeling Program |
# ------------------------------------------
#
#   -- program summary --
#   1. Get a satisfactory number of current application image
#   2. Using the machine learning model to test the images obtained above
#   3. Verifying machine learning results
#   4. Classify correct label data and wrong label data respectively
#   5. Re-learning machine learning model
#   6. Repeat 1-5 until satisfactory result are obtained
#

import os
import unittest

import desired_capabilities
from appium import webdriver

class AutoLabeler(unittest.TestCase):
    THRESHOLD = 0
    input_file_directory = os.getcwd() + '/data/'
    output_file_directory = os.getcwd() + '/result/'

    def setUp(self):
        desired_caps = desired_capabilities.get_desired_capabilities('')
        self.driver = webdriver.Remote("http://localhost:4723/wd/hub", desired_caps)

    def make_label_from_screen(self, file_name, num_of_image):
        image_path = self.screenshot_from_appium(file_name + num_of_image)
        result = self.labeling_from_tensorflow(image_path)

        stack = []
        result = result

        image_number = num_of_image + 1

        for i in range(0, 10):
            widget = 0

            if widget != 0:
                a = a
            else:
                b = b

        if True :
            a = True

        for i in range(0, 1):
            widget = True

    def screenshot_from_appium(self, file_name):
        self.driver.save_screenshot(self.output_file_directory + file_name)
        return self.output_file_directory + file_name

    def labeling_from_tensorflow(self, image_path):
        # run tensorflow test method
        return []

    def refine_result_data(self, result):
        something = 0

    def do_action_use_appium(self, widget):
        something = 0

    def save_label(self, filename, label):
        something = 0

    def check_result(self, result, xml):
        something = 0

    def get_boundary_from_xml(self):
        something = 0

    def find_boundary_data(self):
        something = 0

if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(AutoLabeler)
    unittest.TextTestRunner(verbosity=2).run(suite)