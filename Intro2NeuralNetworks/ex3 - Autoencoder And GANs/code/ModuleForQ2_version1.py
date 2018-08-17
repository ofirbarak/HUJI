# from __future__ import absolute_import
# from __future__ import division
# from __future__ import print_function

import argparse
import sys, os
import tempfile

import time
from tensorflow.examples.tutorials.mnist import input_data
import tensorflow as tf
import matplotlib.pyplot as plt
import numpy as np
import random
import q1_version2 as q1

INPUT = 28 * 28
# FC1_SIZE = 384
# FC2_SIZE = 100

mnist = input_data.read_data_sets('MNIST_data', one_hot=True)
MNIST_SIZE = mnist.train.images.shape[0]
BATCH_SIZE = 5000
LATENT_SIZE = 100
zs = None

# def encoder(x):
#     with tf.name_scope('encoder'):
#         W_fc1 = weight_variable([INPUT, FC2_SIZE])
#         b_fc1 = bias_variable([FC2_SIZE])
#         h_fc1 = tf.nn.relu(tf.matmul(x, W_fc1) + b_fc1)
#     return h_fc1
#
#
# def decoder(h_fc1):
#     with tf.name_scope('decoder'):
#         W_fc4 = weight_variable([FC2_SIZE, INPUT])
#         b_fc4 = bias_variable([INPUT])
#         h_fc4 = tf.nn.sigmoid(tf.matmul(h_fc1, W_fc4) + b_fc4)
#     return h_fc4
#
#
# def weight_variable(shape):
#     """weight_variable generates a weight variable of a given shape."""
#     initial = tf.truncated_normal(shape, stddev=0.1)
#     return tf.Variable(initial)
#
#
# def bias_variable(shape):
#     """bias_variable generates a bias variable of a given shape."""
#     initial = tf.constant(0.1, shape=shape)
#     return tf.Variable(initial)


# def get_image_as_autoecode_result(mnist_image):
#     # Create the model
#     x = tf.placeholder(tf.float32, [None, INPUT])
#
#     # Build the graph for the deep net
#     zs = encoder(x)
#     output = decoder(zs)
#
#     # Create a saver
#     saver = tf.train.Saver()
#
#     with tf.Session() as sess:
#         saver.restore(sess, './savedModel/encoder.ckpt')
#         return sess.run(output, feed_dict={x: mnist_image})
#
#
# def return_sampled_mnist():
#     # sample an image (uniformly) from mnist and return the result from the decoder of the autoencoder
#     random.seed(time.time)
#     i = random.randint(0, MNIST_SIZE)
#     batch_x = None
#     for j in range(0, i, BATCH_SIZE):
#         batch_x, _ = mnist.train.next_batch(BATCH_SIZE)
#     return get_image_as_autoecode_result(batch_x[i % BATCH_SIZE].reshape(1, 784))


# def get_image_as_latent_vec(mnist_image):
#     # Create the model
#     x = tf.placeholder(tf.float32, [None, INPUT])
#
#     # Build the graph for the deep net
#     zs = encoder(x)
#     output = decoder(zs)
#
#     vars = tf.trainable_variables()
#     e_params = [v for v in vars if v.name.startswith('encoder')]
#
#     # print(e_params)
#
#     # Create a saver (for restoring the weights)
#     saver = tf.train.Saver(e_params)
#     with tf.Session() as sess:
#         sess.run(tf.global_variables_initializer())
#         saver.restore(sess, './savedModel/encoder.ckpt')
#         # return
#         return sess.run(zs, feed_dict={x: mnist_image.reshape(1,784)})


def return_sampled_z(batch_size):
    # random.seed(time.time)
    # i = random.randint(0, MNIST_SIZE)
    indexes = np.random.uniform(0., 1., size=[batch_size,])*MNIST_SIZE
    indexes = indexes.astype(np.int)
    return zs[indexes]


from tensorflow.python.tools import inspect_checkpoint as chkp


def main():
    global zs
    zs = np.load('./savedModel/mnist_zs.npy')


if __name__ == "__main__":
    # # chkp.print_tensors_in_checkpoint_file("./savedModel/encoder.ckpt", tensor_name='encoder1/Variable', all_tensors=False)
    # Create the model
    x = tf.placeholder(tf.float32, [None, INPUT])

    # Build the graph for the deep net
    zs = q1.encoder(x)
    output = q1.decoder(zs)

    # Create a saver
    vars = tf.trainable_variables()
    e_params = [v for v in vars if v.name.startswith('encoder')]
    saver = tf.train.Saver(e_params)

    mnist_zs = np.zeros((MNIST_SIZE, LATENT_SIZE))
    with tf.Session() as sess:
        sess.run(tf.global_variables_initializer())
        saver.restore(sess, './savedModel/encoder.ckpt')
        batch = None
        for i in range(int(MNIST_SIZE/BATCH_SIZE)):
            batch = mnist.train.next_batch(BATCH_SIZE)
            print(i, MNIST_SIZE/BATCH_SIZE)
            for j in range(BATCH_SIZE):
                z = sess.run(zs, feed_dict={x: batch[0][i].reshape(1,INPUT)})
                mnist_zs[i*BATCH_SIZE+j:]=z
    np.save('./savedModel/mnist_zs.npy', mnist_zs)


    #     # print(mnist_zs[0])
    # print(return_sampled_z(50).shape)

    # c = np.load('./savedModel/mnist_zs.npy')
    # print(c==mnist_zs)
