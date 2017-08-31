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
import time

from appium import webdriver
from appium.webdriver.common.touch_action import TouchAction

#import Evaluation
import Parser
import desired_capabilities


class AutoLabeler:
    def __init__(self, output_file_directory):
        self.THRESHOLD = 0
        self.output_file_directory = output_file_directory

        self.xml_source = {}
        self.file_name_list = []

        self.desired_caps = desired_capabilities.get_desired_capabilities('../ApiDemos-debug.apk')
        self.driver = webdriver.Remote("http://localhost:4723/wd/hub", self.desired_caps)

        self.label_map_dict = ['Unknown', 'Button', 'EditText', 'CheckBox', 'Option', 'Swipe', 'Switch', 'Spinner']

    ######################
    # Under Construction #
    ######################
    def make_label_from_screen(self, file_name, num_of_image):
        try:
            file_path = self.output_file_directory + file_name + '_' + str(num_of_image)

            time.sleep(0.5)
            self.driver.save_screenshot(file_path)                      # Save current application screen
            self.xml_source[file_name + '_' + str(num_of_image)] = self.driver.page_source  # Save xml source code

            self.do_action_use_appium('BACK')

            self.file_name_list.append(file_name + '_' + str(num_of_image))
            num_of_image = num_of_image+1

        # self.make_label_from_screen(file_name, num_of_image)
        except:
            print ('error occured!')
        finally:
            self.driver.quit()

    ###############
    # Complete??? #
    ###############
    def do_action_use_appium(self, input_widget):
        if input_widget == 'BACK':
            self.driver.press_keycode(4)    # go back
        else:
            x = input_widget
            y = input_widget
            # el = self.driver.find_element_by_name(input_widget)
            action = TouchAction(self.driver)
            action.tap(None, x, y).perform()

    ###################
    # not Complete!!! #
    ###################
    # TODO Use Tensorflow object detection!!
    def labeling_from_tensorflow(self, eval_image_path):
        #evaluation = Evaluation.Evaluation(eval_image_path)
        #tensor_output = evaluation.run()

        tensor_output = [{'name': 'sample_0', 'classes': ['Button', 'Spinner', 'Option'],
                          'boundaries': [[0, 0, 50, 50], [50, 50, 100, 100], [100, 100, 200, 200]],
                          'accuracy': [0.9, 0.8, 0.5]}]
                         # {'name': eval_image_path, 'classes': ['Button', 'Button', 'EditText'],
                         # 'boundaries': [[0, 0, 50, 50], [50, 50, 100, 100], [100, 100, 200, 200]],
                         # 'accuracy': [0.7, 0.6, 0.05]},
                         # {'name': eval_image_path, 'classes': ['Option', 'Option', 'Option'],
                         # 'boundaries': [[0, 0, 50, 50], [50, 50, 100, 100], [100, 100, 200, 200]],
                         # 'accuracy': [0.56, 0.55, 0.2]}]
        return tensor_output   # return refined label data

    ###############
    # Complete!!! #
    ###############
    # result: output from the tensorflow
    def refine_result_data(self, tensor_output):
        image_list = []

        for output_index in range(0, len(tensor_output)):      # do every images
            set_of_widget_type = tensor_output[output_index]['classes']
            set_of_boundaries = tensor_output[output_index]['boundaries']

            label = ''
            for j in range(0, len(set_of_widget_type)):
                line = set_of_widget_type[j] + " 0.0 0 0.0 0 " \
                       + str(set_of_boundaries[j][0]) + " " + str(set_of_boundaries[j][1]) + " " \
                       + str(set_of_boundaries[j][2]) + " " + str(set_of_boundaries[j][3]) \
                       + " 0.0 0.0 0.0 0.0 0.0 0.0\n"

                label = label + line
            image_list.append(label)

        return image_list

    ###############
    # Complete!!! #
    ###############
    def save_label(self, filename, image_label_list):

        for label_index in range(0, len(image_label_list)):
            label_file = open(self.output_file_directory + filename + '_' + str(label_index) + '.txt', 'w')
            label_file.write(image_label_list[label_index])
            label_file.close()
            print('file [' + filename + '] generation complete')

    ###############
    # Complete!!! #
    ###############################################################
    # parm: output <- tensorflow output                           #
    #       file_name <- file name of the saved image(or label)   #
    ###############################################################
    def check_result(self, output_label):
        boundary_list = self.get_boundary_from_xml(self.xml_source[output_label['name']])

        exist_widget_index = []
        non_exist_widget_index = []

        for label_index in range(0, len(output_label)):          # do one image
            index = self.find_boundary_data(output_label, boundary_list)

            if index >= 0:
                exist_widget_index.append(label_index)
            else:
                non_exist_widget_index.append(label_index)

        existence_ratio = float(len(exist_widget_index)) / float(len(exist_widget_index) + len(non_exist_widget_index))

        return exist_widget_index, non_exist_widget_index, existence_ratio

    ###############
    # Complete!!! #
    #############################################################
    # parm: xml_source <- extracted xml source code by appium   #
    #############################################################
    def get_boundary_from_xml(self, xml_source):
        parsing_data = Parser.Parser(xml_source)
        widget_list = parsing_data.parser()

        boundaries = []
        for single_widget in widget_list:
            boundaries.append(single_widget['bounds'])

        return boundaries

    ##############
    # Complete!! #
    #####################################################################
    # Returns True if the label entered as input matches the boundaries #
    # of the widgets in the widget list, otherwise returns False.       #
    # parm: labeled_data <- widget data from output                     #
    #       widget_list <- widget list from xml parsing                 #
    #####################################################################
    def find_boundary_data(self, labeled_data, widget_list):
        label_boundary = labeled_data['boundaries']

        difference_threshold = 250
        min_diff = 9999999
        min_index = 0

        for label_index in range(0, len(label_boundary)):
            for widget_index in range(0, len(widget_list)):
                boundary = widget_list[widget_index]

                difference = 0

                for j in range(0, len(boundary)):
                    temp_diff = int(float(boundary[j])) - int(float(label_boundary[label_index][j]))
                    difference = difference + abs(temp_diff)

                if min_diff > difference:
                    min_diff = difference
                    min_index = widget_index

        if min_diff < difference_threshold:
            return min_index
        else:
            return -1

# main
if __name__ == '__main__':
    image_path = '/home/mllab/test_image/'
    application_name = 'sample'

    auto_labeler = AutoLabeler(image_path)
    auto_labeler.make_label_from_screen(application_name, 0)        # Make image file & xml source list

    result = auto_labeler.labeling_from_tensorflow(image_path)      # output <- list(dictionary) data
    label_data = auto_labeler.refine_result_data(result)            # output <- widget_list data
    auto_labeler.save_label(application_name, label_data)

    for i in range(0, len(result)):
        (exist, non_exist, ratio) = auto_labeler.check_result(result[i])

        if ratio >= 0.5:
            os.system('mv ' + image_path + result[i]['name'] + ' '
                      + image_path + 'accurate/')
            os.system('mv ' + image_path + result[i]['name'] + '.* '
                      + image_path + 'accurate/')
        else:
            os.system('mv ' + image_path + result[i]['name'] + ' '
                      + image_path + 'inaccurate/')
            os.system('mv ' + image_path + result[i]['name'] + '.* '
                      + image_path + 'inaccurate/')

