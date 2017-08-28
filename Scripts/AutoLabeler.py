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

        self.xml_source = {}

        self.desired_caps = desired_capabilities.get_desired_capabilities('')
        self.driver = webdriver.Remote("http://localhost:4723/wd/hub", self.desired_caps)


    #######################
    # On the Construction #
    #######################
    def make_label_from_screen(self, file_name, num_of_image):
        file_path = self.output_file_directory + file_name + '_' + num_of_image
        self.driver.save_screenshot(file_path + '.jpeg')
        self.xml_source[file_name+num_of_image] = self.driver.page_source
        self.do_action_use_appium(widget)

        #TODO implement state transition


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


    #######################
    # On the Construction #
    #######################
    def labeling_from_tensorflow(self, image_path):
        # run tensorflow test method
        # TODO Fix Google Object Detection eval Method
        # get box boundary data, class and accuracy

        box_boundary = []
        classes = []
        accuracy = []

        output = [box_boundary, classes, accuracy]

        return output   # return refined label data


    #######################
    # On the Construction #
    #######################
    # result: output from the tensorflow
    def refine_result_data(self, output):
        label_data = []
        for i in range(0, len(output)):
            widget_type = output.get_widget_type()
            x = output.get_boundary().get_coordinate()
            y = output.get_boundary().get_coordinate()
            width = output.get_boundary().get_width()
            height = output.get_boundary().get_height()

            line = widget_type + " 0.0 0 0.0 0 " \
                   + x + " " + y + " " \
                   + width + " " + height + " 0.0 0.0 0.0 0.0 0.0 0.0\n"

            label_data.append(line)

        return label_data



    ###############
    # COMPLETE!!! #
    ###############
    def save_label(self, filename, label):
        label_file = open(self.output_file_directory + filename, 'w')
        label_file.write(label)
        label_file.close()
        print('file [' + filename + '] generation complete')


    #######################
    # On the Construction #
    #######################
    def check_result(self, output, file_name):
        parser = Parser.Parser(self.xml_source[file_name])
        widget_list = parser.do_parsing()

        for i in range(0, len(output)):
            self.find_boundary_data(output[i], widget_list)


    ###############
    # COMPLETE!!! #
    ###############
    def get_boundary_from_xml(self, xml_source):
        parsing_data = Parser.Parser(xml_source)
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

            for j in range(0, len(boundary)):
                if boundary[j] - label_boundary[j] > 50 :
                    return False

        return True


if __name__ == '__main__':
    auto_labeler = AutoLabeler()
    application_name = ''
    auto_labeler.make_label_from_screen(application_name, 0)

    result = auto_labeler.labeling_from_tensorflow(os.getcwd() + '/result/')
    label_data = auto_labeler.refine_result_data(result)
    auto_labeler.save_label(application_name, label_data)

    auto_labeler.check_result(label_data)
