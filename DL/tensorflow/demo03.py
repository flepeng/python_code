# -*- coding: utf-8 -*-
# @Time    : 2018/9/19 17:02
# @Author  : melon

import tensorflow as tf


"""重复变量的使用"""

# 方式一
def my_func(x):
    w1 = tf.Variable(tf.random_normal([1]))[0]
    b1 = tf.Variable(tf.random_normal([1]))[0]
    r1 = w1 * x + b1

    w2 = tf.Variable(tf.random_normal([1]))[0]
    b2 = tf.Variable(tf.random_normal([1]))[0]
    r2 = w2 * r1 + b2

    return r1, w1, b1, r2, w2, b2

# 方式二
def my_funcc(x):
    # w = tf.Variable(tf.random_normal([1]), name='w')[0]
    # b = tf.Variable(tf.random_normal([1]), name='b')[0]
    w = tf.get_variable(name='w', shape=[1], initializer=tf.random_normal_initializer())[0]
    b = tf.get_variable(name='b', shape=[1], initializer=tf.random_normal_initializer())[0]
    r = w * x + b

    return r, w, b

# 方式三
def func(x):
    with tf.variable_scope('op1', reuse=tf.AUTO_REUSE):
        r1 = my_func(x)
    with tf.variable_scope('op2', reuse=tf.AUTO_REUSE):
        r2 = my_func(r1[0])
    return r1, r2

if __name__ == '__main__':

    # x = tf.constant(3, dtype=tf.float32)
    # r = my_func(x)
    #
    # with tf.Session(config=tf.ConfigProto(log_device_placement=True, allow_soft_placement=True)) as sess:
    #    tf.global_variables_initializer().run()
    #    print(sess.run(r))

    x1 = tf.constant(3, dtype=tf.float32, name='x1')
    x2 = tf.constant(4, dtype=tf.float32, name='x2')
    # my_funcc(x1)
    # 报错
    # my_funcc(x2)
    with tf.variable_scope('func1'):
        r1 = my_funcc(x1)
    with tf.variable_scope('func2'):
        r2 = my_funcc(x2)