# Copyright 2015 The TensorFlow Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================

"""A deep MNIST classifier using convolutional layers.
See extensive documentation at
https://www.tensorflow.org/get_started/mnist/pros
"""
# Disable linter warnings to maintain consistency with tutorial.
# pylint: disable=invalid-name
# pylint: disable=g-bad-import-order

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import argparse
import sys
import tempfile

from tensorflow.examples.tutorials.mnist import input_data

import tensorflow as tf

import matplotlib.pyplot as plt

import time

import numpy as np

FLAGS = None


def deepnn(x):
    """deepnn builds the graph for a deep net for classifying digits.
  Args:
    x: an input tensor with the dimensions (N_examples, 784), where 784 is the
    number of pixels in a standard MNIST image.
  Returns:
    A tuple (y, keep_prob). y is a tensor of shape (N_examples, 10), with values
    equal to the logits of classifying the digit into one of 10 classes (the
    digits 0-9). keep_prob is a scalar placeholder for the probability of
    dropout.
  """
    # Reshape to use within a convolutional neural net.
    # Last dimension is for "features" - there is only one here, since images are
    # grayscale -- it would be 3 for an RGB image, 4 for RGBA, etc.
    channels = 8
    kernel_size = 8
    with tf.name_scope('reshape'):
        x_image = tf.reshape(x, [-1, 28, 28, 1])

    # First convolutional layer - maps one grayscale image to 32 feature maps.
    with tf.name_scope('conv1'):
        W_conv1 = weight_variable([kernel_size, kernel_size, 1, channels])
        b_conv1 = bias_variable([channels])
        h_conv1 = tf.nn.relu(conv2d(x_image, W_conv1) + b_conv1)

    # Dropout - controls the complexity of the model, prevents co-adaptation of
    # features.
    with tf.name_scope('dropout'):
        keep_prob = tf.placeholder(tf.float32)
        h_fc1_drop = tf.nn.dropout(h_conv1, keep_prob)

    # Fully connected layer 1 -- 28x28 image with k channels fully
    # connected to 10 neurons
    with tf.name_scope('fc1'):
        W_fc1 = weight_variable([28 * 28 * channels, 10])
        b_fc1 = bias_variable([10])

        h_conv1_flat = tf.reshape(h_fc1_drop, [-1, 28 * 28 * channels])
        h_fc1 = tf.nn.relu(tf.matmul(h_conv1_flat, W_fc1) + b_fc1)

    return h_fc1, keep_prob


def conv2d(x, W):
    """conv2d returns a 2d convolution layer with full stride."""
    return tf.nn.conv2d(x, W, strides=[1, 1, 1, 1], padding='SAME')


def weight_variable(shape):
    """weight_variable generates a weight variable of a given shape."""
    initial = tf.truncated_normal(shape, stddev=0.1)
    return tf.Variable(initial)


def bias_variable(shape):
    """bias_variable generates a bias variable of a given shape."""
    initial = tf.constant(0.1, shape=shape)
    return tf.Variable(initial)


def main(_):
    # Import data
    mnist = input_data.read_data_sets(FLAGS.data_dir, one_hot=True)

    # Create the model
    x = tf.placeholder(tf.float32, [None, 784])

    # Define loss and optimizer
    y_ = tf.placeholder(tf.float32, [None, 10])

    # Build the graph for the deep net
    y_conv, keep_prob = deepnn(x)

    with tf.name_scope('loss'):
        cross_entropy = tf.nn.softmax_cross_entropy_with_logits(labels=y_,
                                                                logits=y_conv)
    cross_entropy = tf.reduce_mean(cross_entropy)

    with tf.name_scope('adam_optimizer'):
        train_step = tf.train.AdamOptimizer(1e-4).minimize(cross_entropy)

    with tf.name_scope('accuracy'):
        correct_prediction = tf.equal(tf.argmax(y_conv, 1), tf.argmax(y_, 1))
        correct_prediction = tf.cast(correct_prediction, tf.float32)
    accuracy = tf.reduce_mean(correct_prediction)

    graph_location = tempfile.mkdtemp()
    print('Saving graph to: %s' % graph_location)
    train_writer = tf.summary.FileWriter(graph_location)
    train_writer.add_graph(tf.get_default_graph())

    with tf.Session() as sess:
        sess.run(tf.global_variables_initializer())
        train_accuracy = []
        iterations = []
        total_time = 0

        for i in range(5500):
            batch = mnist.train.next_batch(50)
            if i % 100 == 0:
                print(i)
                iterations.append(i)
                train_accuracy.append(accuracy.eval(feed_dict={
                    x: batch[0], y_: batch[1], keep_prob: 1.0}))
            start = time.time()
            train_step.run(feed_dict={x: batch[0], y_: batch[1], keep_prob: 0.5})
            end = time.time()
            total_time += end - start

        test_accuracy = (calc_test_accuracy(accuracy, mnist, x, y_, keep_prob))

        # plot the results, 2 graphs, one for training and one for the testing
        plt.plot(iterations, train_accuracy, '-', label='train accuracy')
        plt.xlabel('iterations')
        plt.ylabel('percentage of success on testing batch')
        plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3,
                   ncol=2, mode="expand", borderaxespad=0.)
        plt.show()
        print("The final test accuracy is: ", test_accuracy)
        print("Elapsed time is: ", total_time)


def calc_test_accuracy(accuracy, mnist, x, y_, keep_prob):
    n_batches = mnist.test.images.shape[0] // 50
    cumulative_accuracy = 0.0
    for index in range(n_batches):
        batch = mnist.test.next_batch(50)
        cumulative_accuracy += accuracy.eval(
            feed_dict = {x: batch[0], y_: batch[1], keep_prob: 1.0})
    print("test accuracy {}".format(cumulative_accuracy / n_batches))
    return cumulative_accuracy / n_batches


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--data_dir', type=str,
                        default='/tmp/tensorflow/mnist/input_data',
                        help='Directory for storing input data')
    FLAGS, unparsed = parser.parse_known_args()
    tf.app.run(main=main, argv=[sys.argv[0]] + unparsed)

"""
The final test accuracy is:  0.960500000715
Elapsed time is:  98.51398181915283
"""