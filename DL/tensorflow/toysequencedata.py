# -*- coding: utf-8 -*-
# @Time    : 2019/1/22 14:37
# @Author  : melon

import tensorflow as tf
import random
import numpy as np

class ToySequenceData(object):
    """
    -类别0:[0, 1, 2, 3...]
    -类别1:[1, 3, 10, 7]
    """
    def __init__(self, n_samples=1000, max_seq_len=20, min_seq_len=3, max_value=1000):
        self.data = []
        self.labels = []
        # 未补0的数列的真正长度
        self.seqlen = []
        self.batch_id = 0
        for i in range(n_samples):
            len = random.randint(min_seq_len, max_seq_len)
            self.seqlen.append(len)
            if random.random() < 0.5:
                rand_start = random.randint(0, max_value - len)
                s = [[float(i)/max_value] for i in range(rand_start, rand_start+len)]
                s += [[0.] for i in range(max_seq_len-len)]
                self.data.append(s)
                self.labels.append([1.0, 0.0])
            else:
                s = [[float(random.randint(0, max_value))/max_value] for i in range(len)]
                s += [[0.] for i in range(max_seq_len-len)]
                self.data.append(s)
                self.labels.append([0., 1.])

    def next(self, batch_size):

        if self.batch_id == len(self.data):
            self.batch_id = 0
        batch_data = (self.data[self.batch_id:min(self.batch_id+batch_size, len(self.data))])
        batch_labels = (self.labels[self.batch_id:min(self.batch_id+batch_size, len(self.data))])
        batch_seqlen = (self.seqlen[self.batch_id:min(self.batch_id + batch_size, len(self.data))])
        self.batch_id = min(self.batch_id + batch_size, len(self.data))
        return batch_data, batch_labels, batch_seqlen


if __name__ == '__main__':

    learning_rate = 0.01
    training_iters = 100000
    batch_size = 128
    display_step = 10

    # 网络参数
    seq_max_len = 20
    n_hidden = 64
    n_classes = 2

    trainset = ToySequenceData(n_samples=1000, max_seq_len=seq_max_len)
    testset = ToySequenceData(n_samples=500, max_seq_len=seq_max_len)

    x = tf.placeholder(tf.float32, [None, seq_max_len, 1])
    y = tf.placeholder(tf.float32, [None, n_classes])
    seqlen = tf.placeholder(tf.int32, [None])

    # 正态分布初始化参数
    weights = {'out': tf.Variable(tf.random_normal([n_hidden, n_classes]))}
    biases = {'out': tf.Variable(tf.random_normal([n_classes]))}


    def dynamicRNN(x, seqlen, weights, biases):

        lstm_cell = tf.nn.rnn_cell.BasicLSTMCell(n_hidden)
        # 每个step的输出值以及最终的状态
        outputs, states = tf.nn.dynamic_rnn(lstm_cell, x, dtype=tf.float32, sequence_length=seqlen)
        batch_size = tf.shape(outputs)[0]
        index = tf.range(0, batch_size) * seq_max_len + (seqlen - 1)
        outputs = tf.gather(tf.reshape(outputs, [-1, n_hidden]), index)
        return tf.matmul(outputs, weights['out']) + biases['out']

    pred = dynamicRNN(x, seqlen, weights, biases)
    cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=pred, labels=y))
    optimizer = tf.train.GradientDescentOptimizer(learning_rate=learning_rate).minimize(cost)
    correct_pred = tf.equal(tf.argmax(pred, 1), tf.argmax(y, 1))
    accuracy = tf.reduce_mean(tf.cast(correct_pred, tf.float32))

    init = tf.global_variables_initializer()

    with tf.Session() as sess:
        sess.run(init)
        step = 1
        while step * batch_size < training_iters:
            batch_x, batch_y, batch_seqlen = trainset.next(batch_size)
            sess.run(optimizer, feed_dict={x: batch_x, y: batch_y, seqlen: batch_seqlen})
            if step % 10 == 0:
                pre = sess.run(pred, feed_dict={x: batch_x, y: batch_y, seqlen: batch_seqlen})
                print("预测值:" + str(pre))
                acc = sess.run(accuracy, feed_dict={x: batch_x, y: batch_y, seqlen: batch_seqlen})
                loss = sess.run(cost, feed_dict={x: batch_x, y: batch_y, seqlen: batch_seqlen})
                print("Iter" + str(step * batch_size) + ", Minibatch Loss = " + \
                        "{:.6f}".format(loss) + ", Training Accuracy= " + \
                        "{:.5f}".format(acc))
            step += 1
            print("训练步数:" + str(step))


        print("Optimization Finished!")

        test_data = testset.data
        test_label = testset.labels
        testset_seqlen = testset.seqlen
        print("Testing Accuracy:", sess.run(accuracy, feed_dict={x: test_data, y: test_label, seqlen: testset_seqlen}))

























