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

from appium import webdriver
from appium.webdriver.common.touch_action import TouchAction
import desired_capabilities

import widget
import Parser

class AutoLabeler:
    def __init__(self):
        self.THRESHOLD = 0
        self.input_file_directory = os.getcwd() + '/data/'
        self.output_file_directory = os.getcwd() + '/result/'

        self.desired_caps = desired_capabilities.get_desired_capabilities('')
        self.driver = webdriver.Remote("http://localhost:4723/wd/hub", self.desired_caps)


    #######################
    # On the Construction #
    #######################
    def make_label_from_screen(self, file_name, num_of_image):
        image_path = self.screenshot_from_appium(file_name + num_of_image)

        #TODO implement state transition



    ###############
    # COMPLETE!!! #
    ###############
    def screenshot_from_appium(self, file_name):
        self.driver.save_screenshot(self.output_file_directory + file_name)
        return self.output_file_directory + file_name


    #######################
    # On the Construction #
    #######################
    def labeling_from_tensorflow(self, image_path):
        # run tensorflow test method
        result = 0
        return result   # return refined label data


    #######################
    # On the Construction #
    #######################
    # result: output from the tensorflow
    def refine_result_data(self, result):
        label_data = []
        for i in range(0, len(result)):
            widget_type = result.get_widget_type()
            x = result.get_boundary().get_coordinate()
            y = result.get_boundary().get_coordinate()
            width = result.get_boundary().get_width()
            height = result.get_boundary().get_height()

            line = widget_type + " 0.0 0 0.0 0 " \
                   + x + " " + y + " " \
                   + width + " " + height + " 0.0 0.0 0.0 0.0 0.0 0.0"

            label_data.append(line)

        return label_data


    ###############
    # COMPLETE!!! #
    ###############
    def do_action_use_appium(self, input_widget):
        if input_widget == 'BACK':
            self.driver.press_keycode(4)    # go back
        else:
            el = self.driver.find_element_by_name(input_widget)
            action = TouchAction(self.driver)
            action.tap(el).perform()

    ###############
    # COMPLETE!!! #
    ###############
    def save_label(self, filename, label):
        label_data = open(self.output_file_directory + filename, 'w')
        label_data.write(label)
        label_data.close()


    #######################
    # On the Construction #
    #######################
    def check_result(self, result):
        xml = self.driver.page_source
        widget_list = self.get_boundary_from_xml()


    ###############
    # COMPLETE!!! #
    ###############
    def get_boundary_from_xml(self):
        xml = self.driver.page_source

        parsing_data = Parser.Parser(xml)
        widget_list = parsing_data.do_parsing()

        boundaries = []
        for i in range(0, len(widget_list)):
            boundaries.append(widget_list[i].get_widget_data('boundary'))

        return boundaries


    #######################
    # On the Construction #
    #######################
    # Returns True if the label entered as input matches the boundaries
    # of the widgets in the widget list, otherwise returns False.
    def find_boundary_data(self, label, widget_list):
        label_boundary = label.get_boundary() # must be implemented!!

        for i in range(0, len(widget_list)):
            single_widget = widget_list[i]
            boundary = single_widget.get_widget_data('boundary')

            for i in range(0, 4):
                if boundary[i] - label_boundary[i] > 50 :
                    return False

        return True