import os
import sys

import numpy as np
import tensorflow as tf
from PIL import Image

sys.path.append("/home/mllab/models/")

from utils import label_map_util


##################
# Data Structure #
#####################################################
#   identified_result   -  result   - classes       #
#                       |    .      - boundaries    #
#                       |    .      - accuracy      #
#                       |    .                      #
#                       -  result   - classes       #
#                                   - boundaries    #
#                                   - accuracy      #
#####################################################

class Evaluation:
    def __init__(self, image_path):
        self.PATH_TO_CKPT = './config/output.pb'
        self.PATH_TO_LABELS = './config/ui_label_map.pbtxt'

        self.NUM_CLASSES = 38

        self.detection_graph = tf.Graph()
        self.path = image_path
        self.label_map_dict = ['Unknown', 'Button', 'EditText', 'CheckBox', 'Option', 'Swipe', 'Switch', 'Spinner']

    def load_image_into_numpy_array(self, image):
        (im_width, im_height) = image.size
        return np.array(image.getdata()).reshape(
            (im_height, im_width, 3)).astype(np.uint8)

    def run(self):
        with self.detection_graph.as_default():
            od_graph_def = tf.GraphDef()
            with tf.gfile.GFile(self.PATH_TO_CKPT, 'rb') as fid:
                serialized_graph = fid.read()
                od_graph_def.ParseFromString(serialized_graph)
                tf.import_graph_def(od_graph_def, name='')

        label_map = label_map_util.load_labelmap(self.PATH_TO_LABELS)
        categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=self.NUM_CLASSES,
                                                                    use_display_name=True)
        category_index = label_map_util.create_category_index(categories)
        identified_result = []

        with self.detection_graph.as_default():
            with tf.Session(graph=self.detection_graph) as sess:
                for image_path in os.listdir(self.path):
                    image = Image.open(os.path.join(self.path, image_path))
                    (width, height) = image.size
                    image_np = self.load_image_into_numpy_array(image)
                    image_np_expanded = np.expand_dims(image_np, axis=0)

                    image_tensor = self.detection_graph.get_tensor_by_name('image_tensor:0')

                    boxes = self.detection_graph.get_tensor_by_name('detection_boxes:0')
                    scores = self.detection_graph.get_tensor_by_name('detection_scores:0')
                    classes = self.detection_graph.get_tensor_by_name('detection_classes:0')
                    num_detections = self.detection_graph.get_tensor_by_name('num_detections:0')

                    (boxes, scores, classes, num_detections) = sess.run(
                        [boxes, scores, classes, num_detections],
                        feed_dict={image_tensor: image_np_expanded})

                    result = {'name': image_path, 'classes': [], 'boundaries': [], 'accuracy': []}

                    for i in range(0, len(boxes)):
                        for j in range(0, len(boxes[i])):
                            if scores[i][j] >= 0.5:
                                temp_bound = [int(float(boxes[i][j][1]) * width),  # x_start
                                              int(float(boxes[i][j][0]) * height),  # y_start
                                              int(float(boxes[i][j][3]) * width),  # x_end
                                              int(float(boxes[i][j][2]) * height)]  # y_end

                                result['boundaries'].append(temp_bound)
                                result['classes'].append(self.label_map_dict[int(float(classes[i][j]))])
                                result['accuracy'].append("{:.5f}".format(scores[i][j]))

                    identified_result.append(result)

        return identified_result
