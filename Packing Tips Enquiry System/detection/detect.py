
import cv2
import os
import shutil
import numpy as np
import tensorflow as tf

import detection.utils as utils
from detection.config import cfg
from detection.yolov3 import YOLOV3

class YoloTest(object):
    def __init__(self):
        self.input_size       = cfg.TEST.INPUT_SIZE
        self.anchor_per_scale = cfg.YOLO.ANCHOR_PER_SCALE
        self.classes          = utils.read_class_names(cfg.YOLO.CLASSES)
        self.num_classes      = len(self.classes)
        self.anchors          = np.array(utils.get_anchors(cfg.YOLO.ANCHORS))
        self.score_threshold  = cfg.TEST.SCORE_THRESHOLD
        self.iou_threshold    = cfg.TEST.IOU_THRESHOLD
        self.moving_ave_decay = cfg.YOLO.MOVING_AVE_DECAY
        self.weight_file      = cfg.YOLO.DEMO_WEIGHT
        self.show_label       = cfg.TEST.SHOW_LABEL
        self.write_path       = cfg.TEST.WRITE_IMAGE_PATH

        with tf.name_scope('input'):
            self.input_data = tf.placeholder(dtype=tf.float32, name='input_data')
            self.trainable  = tf.placeholder(dtype=tf.bool,    name='trainable')

        model = YOLOV3(self.input_data, self.trainable)
        self.pred_sbbox, self.pred_mbbox, self.pred_lbbox = model.pred_sbbox, model.pred_mbbox, model.pred_lbbox

        with tf.name_scope('ema'):
            ema_obj = tf.train.ExponentialMovingAverage(self.moving_ave_decay)

        self.classes = utils.read_class_names(cfg.YOLO.CLASSES)

        self.sess  = tf.Session(config=tf.ConfigProto(allow_soft_placement=True))
        self.saver = tf.train.Saver(ema_obj.variables_to_restore())
        self.saver.restore(self.sess, self.weight_file)

    def predict(self, image):
        org_image = np.copy(image)
        org_h, org_w, _ = org_image.shape

        image_data = utils.image_preporcess(image, [self.input_size, self.input_size])
        image_data = image_data[np.newaxis, ...]

        pred_sbbox, pred_mbbox, pred_lbbox = self.sess.run(
            [self.pred_sbbox, self.pred_mbbox, self.pred_lbbox],
            feed_dict={
                self.input_data: image_data,
                self.trainable: False
            }
        )

        pred_bbox = np.concatenate([np.reshape(pred_sbbox, (-1, 5 + self.num_classes)),
                                    np.reshape(pred_mbbox, (-1, 5 + self.num_classes)),
                                    np.reshape(pred_lbbox, (-1, 5 + self.num_classes))], axis=0)
        bboxes = utils.postprocess_boxes(pred_bbox, (org_h, org_w), self.input_size, self.score_threshold)
        bboxes = utils.nms(bboxes, self.iou_threshold)

        class_names = []
        for bbox in bboxes:
            class_ind = int(bbox[5])
            class_name = self.classes[class_ind]
            class_names.append(class_name)
        return bboxes, class_names

    def draw(self,image, bboxes):
        image = utils.draw_bbox(image, bboxes, show_label=self.show_label)
        if not os.path.exists(self.write_path):
            os.makedirs(self.write_path)
        cv2.imwrite(self.write_path + '/text.png', image)
        return image


if __name__ == '__main__':
    image_path = "../obj.png"
    image = cv2.imread(image_path)
    yolo = YoloTest()
    bboxes, class_names = yolo.predict(image)
    print(class_names)
    image = yolo.draw(image, bboxes)




