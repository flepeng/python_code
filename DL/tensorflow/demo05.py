# -*- coding: utf-8 -*-
# @Time    : 2019/1/18 11:35
# @Author  : melon

from tensorflow.examples.tutorials.mnist import input_data
import tensorflow as tf

"""tensorflow中运用Softmax实现多分类"""

if __name__ == '__main__':
    mnist = input_data.read_data_sets('MNIST_data', one_hot=True)
    print('download......')

    # 初始化变量
    x = tf.placeholder(tf.float32, [None, 784])
    W = tf.Variable(tf.zeros([784, 10]))
    b = tf.Variable(tf.zeros([10]))

    # 模型输出与实际图像值
    y = tf.nn.softmax(tf.matmul(x, W) + b)
    y_ = tf.placeholder(tf.float32, [None, 10])

    # 构造交叉熵损失函数
    cross_entropy = tf.reduce_mean(-tf.reduce_sum(y_ * tf.log(y)))
    # 以0.01的学习率优化损失函数
    train_step = tf.train.GradientDescentOptimizer(0.01).minimize(cross_entropy)

    sess = tf.InteractiveSession()
    tf.global_variables_initializer().run()\

    for _ in range(1000):
        batch_xs, batch_ys = mnist.train.next_batch(100)
        res = sess.run(train_step, feed_dict={x: batch_xs, y_: batch_ys})

    # 计算准确率
    correct_prediction = tf.equal(tf.argmax(y, 1), tf.argmax(y_, 1))
    accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
    print(sess.run(accuracy, feed_dict={x: mnist.test.images, y_: mnist.test.labels}))