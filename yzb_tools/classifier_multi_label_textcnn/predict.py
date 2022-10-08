# -*- coding: utf-8 -*-
"""
Created on Thu May 30 17:12:37 2019

@author: cm
"""


import os
import sys
pwd = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
import numpy as np
import tensorflow as tf
from classifier_multi_label_textcnn.networks import NetworkAlbertTextCNN
from classifier_multi_label_textcnn.classifier_utils import get_feature_test,id2label
from classifier_multi_label_textcnn.hyperparameters import Hyperparamters as hp

          

class ModelAlbertTextCNN(object,):
    """
    Load NetworkAlbert TextCNN model
    """
    def __init__(self):
        self.albert, self.sess = self.load_model()

    @staticmethod
    def load_model():
        with tf.Graph().as_default():
            sess = tf.Session()
            with sess.as_default():
                albert =  NetworkAlbertTextCNN(is_training=False)
                saver = tf.train.Saver()  
                sess.run(tf.global_variables_initializer())
                checkpoint_dir = os.path.abspath(os.path.join(pwd,hp.file_load_model))
                print (checkpoint_dir)
                ckpt = tf.train.get_checkpoint_state(checkpoint_dir)
                saver.restore(sess, ckpt.model_checkpoint_path)
        return albert,sess

MODEL = ModelAlbertTextCNN()
print('Load model finished!')


def get_label(sentence):
    """
    Prediction of the sentence's label.
    """
    feature = get_feature_test(sentence)
    fd = {MODEL.albert.input_ids: [feature[0]],
          MODEL.albert.input_masks: [feature[1]],
          MODEL.albert.segment_ids:[feature[2]],
          }
    prediction = MODEL.sess.run(MODEL.albert.predictions, feed_dict=fd)[0]
    # print(prediction,'prediction')
    r = []
    for i in range(len(prediction)):
        if prediction[i] != 0.0:
            r.append(id2label(i))
    return r[:5]
    # return [id2label(l) for l in np.where(prediction==1)[0] if l!=0]

if __name__ == '__main__':
    # Test
    # from data_clean import get_test_list
    sentences = ['衢州市教育事业发展中心关于2021年衢州市工程技术学校学生寝室床柜采购项目的更正公告',
                 '辽源市人民防空办公室定点服务结果公告',
                 '重庆市江北区城市照明管理所江北嘴大剧院景观照明设施维护服务项目（第二次）(21C00031)中标（成交）结果公告',
                 '内乡县大桥乡老美坡滨水田园小镇安置区续建项目二标',
                 '内乡县大桥乡老美坡滨水田园小镇安置区监理项目',
     ]

    for sentence in sentences:
        print(sentence,get_label(sentence))


    
    
    
    
