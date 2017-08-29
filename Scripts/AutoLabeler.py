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
import TensorOutput
import Evaluation


class AutoLabeler:
    def __init__(self):
        self.THRESHOLD = 0
        self.input_file_directory = os.getcwd() + '/data/'
        self.output_file_directory = os.getcwd() + '/result/'

        self.xml_source = {}

        self.desired_caps = desired_capabilities.get_desired_capabilities('')
        self.driver = webdriver.Remote("http://localhost:4723/wd/hub", self.desired_caps)

        self.label_map_dict = ['Unknown', 'Button', 'EditText', 'CheckBox', 'Option', 'Swipe', 'Switch', 'Spinner']

    ######################
    # Under Construction #
    ######################
    def make_label_from_screen(self, file_name, num_of_image):
        file_path = self.output_file_directory + file_name + '_' + num_of_image
        self.driver.save_screenshot(file_path + '.jpeg')
        self.xml_source[file_name+num_of_image] = self.driver.page_source
        self.do_action_use_appium(widget)

        # TODO implement state transition
        # option 1: User initial sequence << efficient and easy to implement
        # option 2: auto state transition using tensorflow result
        # option 3: auto state transition using xml source

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

    ######################
    # Under Construction #
    ######################
    def labeling_from_tensorflow(self, image_path):
        # run tensorflow test method
        # TODO Fix Google Object Detection eval Method
        # get box boundary data, class and accuracy

        evaluation = Evaluation.Evaluation()
        tensor_output = evaluation.run()

        for single_box in tensor_output:
            boundary = single_box['boundaries']
            identified_class = single_box['classes']
            accuracy = single_box['accuracy']

            refined = TensorOutput.TensorOutput(boundary, identified_class, accuracy)

            tensor_output.append(refined)

        return tensor_output   # return refined label data

    ##############
    # Complete!! #
    ##############
    # result: output from the tensorflow
    def refine_result_data(self, output):
        label_list = []
        for i in range(0, len(output)):
            widget_type = output[i].get_class()

            x_start = output[i].get_boundary()[0]
            y_start = output[i].get_boundary()[1]
            x_end = output[i].get_boundary()[2]
            y_end = output[i].get_boundary()[3]

            line = widget_type + " 0.0 0 0.0 0 " \
                   + x_start + " " + y_start + " " \
                   + x_end + " " + y_end + " 0.0 0.0 0.0 0.0 0.0 0.0\n"

            label_list.append(line)

        return label_list

    ###############
    # COMPLETE!!! #
    ###############
    def save_label(self, filename, label):
        label_file = open(self.output_file_directory + filename, 'w')
        label_file.write(label)
        label_file.close()
        print('file [' + filename + '] generation complete')

    ######################
    # Under Construction #
    #####################################################################
    # parm: output <- output of the refined data (type -> widget_list)  #
    #       file_name <- file name of the saved image(or label)         #
    #####################################################################
    def check_result(self, output, file_name):
        parser = Parser.Parser(self.xml_source[file_name])
        widget_list = parser.do_parsing()

        for i in range(0, len(output)):
            self.find_boundary_data(output[i], widget_list)

    ###############
    # COMPLETE!!! #
    #############################################################
    # parm: xml_source <- extracted xml source code by appium   #
    #############################################################
    def get_boundary_from_xml(self, xml_source):
        parsing_data = Parser.Parser(xml_source)
        widget_list = parsing_data.do_parsing()

        boundaries = []
        for single_widget in widget_list:
            boundaries.append(single_widget.get_widget_data('boundary'))

        return boundaries

    ######################
    # Under Construction #
    #####################################################################
    # Returns True if the label entered as input matches the boundaries #
    # of the widgets in the widget list, otherwise returns False.       #
    # parm: widget_data <- widget data from output                      #
    #       widget_list <- widget list from xml parsing                 #
    #####################################################################
    def find_boundary_data(self, widget_data, widget_list):
        label_boundary = widget_data.get_boundary()  # must be implemented!!

        for single_widget in widget_list:
            boundary = single_widget.get_widget_data('boundary')

            for j in range(0, len(boundary)):
                if boundary[j] - label_boundary[j] > 50:
                    return False

        return True

# main
if __name__ == '__main__':
    auto_labeler = AutoLabeler()
    application_name = ''
    auto_labeler.make_label_from_screen(application_name, 0)

    result = auto_labeler.labeling_from_tensorflow(os.getcwd() + '/result/')    # output <- list(dictionary) data
    label_data = auto_labeler.refine_result_data(result)                        # output <- widget_list data
    auto_labeler.save_label(application_name, label_data)                       # output <- noting

    if auto_labeler.check_result(label_data, application_name):
        do = 0
        something = 0
        # save accurate folder
    else:
        do = 1
        something = 1
        # save inaccurate folder
