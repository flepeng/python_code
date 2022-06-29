# -*- coding: utf-8 -*-
# @Time    : 2018/9/20 10:30
# @Author  : melon

import tensorflow as tf
import numpy as np
from tensorflow.python.framework import ops
import matplotlib.pyplot as plt


"""tensorflow实现线性回归"""

ops.reset_default_graph()

sess = tf.Session()

# 数据数量与批量大小
data_amount = 101
batch_size = 25

# 造数据y=5x+3
x_vals = np.linspace(20, 200, data_amount)
y_vals = np.multiply(x_vals, 5)
y_vals = np.add(y_vals, 3)

# 生成一个N(0, 15)的正太分布一维数组
y_offset_vals = np.random.normal(0, 15, data_amount)

x_data = tf.placeholder(shape=[None, 1], dtype=tf.float32)
y_target = tf.placeholder(shape=[None, 1], dtype=tf.float32)

# 构造K
K = tf.Variable(tf.random_normal(mean=0, shape=[1, 1]))
calcY = tf.add(tf.matmul(x_data, K), 3)

# 真实值与模型估算的差值
loss = tf.reduce_mean(tf.square(y_target - calcY))

init = tf.global_variables_initializer()
sess.run(int)




