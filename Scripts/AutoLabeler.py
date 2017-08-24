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
from appium.webdriver.common.touch_action import TouchAction

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
        result = self.refine_result_data(result)

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
        result = 0
        return result   # return refined label data

    def refine_result_data(self, result):


        return result

    def do_action_use_appium(self, widget):
        if widget == 'BACK':
            self.driver.press_keycode(4)    # go back
        else:
            el = self.driver.find_element_by_name(widget)
            action = TouchAction(self.driver)
            action.tap(el).perform()

    def save_label(self, filename, label):
        label_data = open(self.output_file_directory + filename, 'w')
        label_data.write(label)
        label_data.close()

    def check_result(self, result):
        xml = self.driver.page_source
        widget_list = self.get_boundary_from_xml()


    def get_boundary_from_xml(self):
        xml = self.driver.page_source

        # Parsing Parsing Parsing Parsing Parsing
        # Parsing Parsing Parsing Parsing Parsing
        # Parsing Parsing Parsing Parsing Parsing
        # Parsing Parsing Parsing Parsing Parsing
        # Parsing Parsing Parsing Parsing Parsing
        # Parsing Parsing Parsing Parsing Parsing

        widget_list = []
        return widget_list

    def find_boundary_data(self, label, widget_list):
        a = 1
        # check start_x, start_y, width, height

if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(AutoLabeler)
    unittest.TextTestRunner(verbosity=2).run(suite)