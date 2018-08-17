# from __future__ import absolute_import
# from __future__ import division
# from __future__ import print_function

import argparse
import sys
import tempfile

# import matplotlib
# matplotlib.use('Agg')

import time
from tensorflow.examples.tutorials.mnist import input_data
import tensorflow as tf
import matplotlib.pyplot as plt
import numpy as np
from sklearn.decomposition import PCA, FastICA

FLAGS = None

INPUT = 28 * 28
FC1_SIZE = 384
FC2_SIZE = 100
ITERATIONS = 20000

def Conv2d(input, output_dim=64, kernel=(5, 5), strides=(1,1), stddev=0.2, name='conv_2d'):
    with tf.variable_scope(name):
        W = tf.get_variable('Conv2dW', [kernel[0], kernel[1], input.get_shape()[-1], output_dim],
                            initializer=tf.truncated_normal_initializer(stddev=stddev))
        b = tf.get_variable('Conv2db', [output_dim], initializer=tf.zeros_initializer())

        return tf.nn.conv2d(input, W, strides=[1, strides[0], strides[1], 1], padding='SAME') + b


def FC(input, dims, name):
    idims = input.get_shape()
    x = int(idims[0]*idims[1]*idims[2])
    y = int(dims[0]*dims[1]*dims[2])
    print(x)

    D_rshape1 = tf.reshape(input, [-1 ,x])
    D_dense = Dense(D_rshape1, y, name=name)
    D_rshape2 = tf.reshape(D_dense, [-1, dims[0], dims[1], dims[2]])
    return D_rshape2




def encoder(X):
    with tf.name_scope('encoder'):
        E_reshaped = tf.reshape(X, [-1, 28, 28, 1])
        E_conv1 = Conv2d(E_reshaped, output_dim=4, name='encoder/E_conv1')
        E_relu1 = tf.nn.relu(E_conv1)
        E_maxpool1 = tf.nn.max_pool(E_relu1, ksize=[1,2,2,1], strides=[1,2,2,1], padding='SAME')
        E_conv2 = Conv2d(E_maxpool1, output_dim=8, name='encoder/E_conv2')
        E_relu2 = tf.nn.relu(E_conv2)
        E_maxpool2 = tf.nn.max_pool(E_relu2, ksize=[1,2,2,1], strides=[1,2,2,1], padding='SAME')
        E_conv3 = Conv2d(E_maxpool2, output_dim=16, name='encoder/E_conv3')
        E_relu3 = tf.nn.relu(E_conv3)
        E_maxpool3 = tf.nn.max_pool(E_relu3, ksize=[1,2,2,1], strides=[1,2,2,1], padding='SAME')
        E_rshape1 = tf.reshape(E_maxpool3, [-1, 4*4*16])
        E_dense1 = Dense(E_rshape1, 100, name='encoder/E_fc1')
    return E_dense1




def decoder(Z):
    with tf.name_scope('Decoder'):
        Z = tf.reshape(Z, [-1,100])
        D_fc1 = tf.layers.dense(inputs=Z, units=14*14*8, activation=tf.nn.relu )
        D_fc1_r = tf.reshape(D_fc1, [-1,14,14,8])
        D_conv1 = tf.layers.conv2d(
            inputs=D_fc1_r,
            filters=8,
            kernel_size=[3, 3],
            padding="same",
            activation=tf.nn.relu)
        D_conv1_r = tf.reshape(D_conv1, [-1,14*14*8])
        D_fc2 = tf.layers.dense(inputs=D_conv1_r, units=28*28*4, activation=tf.nn.relu )
        D_fc2_r = tf.reshape(D_fc2, [-1,28,28,4])
        #dropout = tf.layers.dropout(
        #    inputs=D_fc2_r, rate=0.4, training= tf.estimator.ModeKeys.TRAIN)
        D_conv2 = tf.layers.conv2d(
            inputs=D_fc2_r ,
            filters=1,
            kernel_size=[3, 3],
            padding="same",
            activation=tf.nn.relu)
    return tf.reshape(D_conv2, [-1,28*28])


def decoder2(Z):
    with tf.name_scope('decoder'):
        Z = tf.reshape(Z, [-1,1,1,100])
        # print(Z.shape)
        D_fc1 = FC(Z, [-1,4,4,16], name='decoder/D_fc1')
        D_conv1 = Conv2d(D_fc1, output_dim=16, name='decoder/D_conv1')
        D_relu1 =tf.nn.relu(D_conv1)
        D_fc2 = FC(D_relu1, [-1,7, 7, 16], name='decoder/D_fc2')
        D_conv2 = Conv2d(D_fc2, output_dim=8, name='decoder/D_conv2')
        D_relu2 = tf.nn.relu(D_conv2)
        D_fc3 = FC(D_relu2, [-1,14, 14, 8], name='decoderD_fc3')
        D_conv3 = Conv2d(D_fc3, output_dim=4, name='decoder/D_conv3')
        D_relu3 = tf.nn.relu(D_conv3)
        D_fc4 = FC(D_relu3, [-1,28, 28, 4], name='decoder/D_fc4')
        D_conv4 = Conv2d(D_fc4, output_dim=1, name='decoder/D_conv4')
    return D_conv4


def Dense(input, output_dim, stddev=0.02, name='dense'):
    with tf.variable_scope(name):
        shape = input.get_shape()
        W = tf.get_variable('DenseW', [shape[1], output_dim], tf.float32,
                            tf.random_normal_initializer(stddev=stddev))
        b = tf.get_variable('Denseb', [output_dim],
                            initializer=tf.zeros_initializer())

        return tf.matmul(input, W) + b

def main():
    # Import data
    mnist = input_data.read_data_sets('MNIST_data', one_hot=True)
    # Create the model
    x = tf.placeholder(tf.float32, [None, INPUT])

    # Build the graph for the deep net
    fc3 = encoder(x)
    output = decoder(fc3)

    vars = tf.trainable_variables()
    e_params = [v for v in vars if v.name.startswith('encoder')]
    d_params = [v for v in vars if v not in e_params]
    # Create a saver
    e_saver = tf.train.Saver(e_params)
    d_saver = tf.train.Saver(d_params)

    with tf.name_scope('loss'):
        loss = tf.reduce_mean(tf.nn.l2_loss(output - x)) + 10e-5 * tf.reduce_sum(tf.abs(output - x))
        # output=tf.clip_by_value(output, 1e-7, 1. - 1e-7)
        # loss = tf.reduce_mean(tf.nn.sigmoid_cross_entropy_with_logits(logits=output, labels=x))

    with tf.name_scope('adam_optimizer'):
        optimizer = tf.train.AdamOptimizer(1e-3).minimize(loss)

    graph_location = tempfile.mkdtemp()
    print('Saving graph to: %s' % graph_location)
    train_writer = tf.summary.FileWriter(graph_location)
    train_writer.add_graph(tf.get_default_graph())

    latent_mat = np.zeros((1, 100))
    labels = np.zeros((1, 1))

    with tf.Session() as sess:
        sess.run(tf.global_variables_initializer())
        for i in range(ITERATIONS + 1):
            batch_x, batch_y = mnist.train.next_batch(50)
            _, l = sess.run([optimizer, loss], feed_dict={x: batch_x})
            if i % 100 == 0:
                print("iteration: %d, train_loss: %f" % (i, l))

            a = np.array(list(map(lambda y: np.argmax(y), batch_y)))
            a = a.reshape((50, 1))
            labels = np.concatenate((labels, a))

            latent_vecs = sess.run(fc3, feed_dict={x: batch_x})
            latent_mat = np.concatenate((latent_mat, latent_vecs))

        # save the model
        e_saver.save(sess, './savedModel/encoder.ckpt')
        d_saver.save(sess, './savedModel/decoder.ckpt')

        if True:
            # Testing
            # Encode and decode images from test set and visualize their reconstruction.
            n = 5
            canvas_orig = np.empty((28 * n, 28 * n))
            canvas_recon = np.empty((28 * n, 28 * n))
            for i in range(n):
                # MNIST test set
                batch_x, _ = mnist.test.next_batch(n)
                # Encode and decode the digit image
                g = sess.run(output, feed_dict={x: batch_x})

                # Display original images
                for j in range(n):
                    # Draw the original digits
                    canvas_orig[i * 28:(i + 1) * 28, j * 28:(j + 1) * 28] = \
                        batch_x[j].reshape([28, 28])
                # Display reconstructed images
                for j in range(n):
                    # Draw the reconstructed digits
                    canvas_recon[i * 28:(i + 1) * 28, j * 28:(j + 1) * 28] = \
                        g[j].reshape([28, 28])

            print("Original Images")
            plt.figure(figsize=(n, n))
            plt.imshow(canvas_orig, origin="upper", cmap="gray")
            plt.show()
            plt.savefig('./output/' + 'Original_Images.png')

            print("Reconstructed Images")
            plt.figure(figsize=(n, n))
            plt.imshow(canvas_recon, origin="upper", cmap="gray")
            plt.show()
            plt.savefig('./output/' + 'Reconsructed_Images.png')

    # visualize PCA
    latent_mat = latent_mat[1:]
    labels = labels[1:]

    pca = PCA(n_components=2)
    results = pca.fit_transform(latent_mat)
    rx, ry = results[:, 0], results[:, 1]
    # print(rx.shape, ry.shape)
    rx = rx.reshape((len(rx), 1))
    ry = ry.reshape((len(ry), 1))

    colors = ['blue', 'orange', 'green', 'red', 'purple', 'brown', 'pink', 'gray', 'olive', 'cyan']
    for i in range(10):
        group_labels = labels == i
        # print(group_labels.shape)
        # print(rx[group_labels].shape)

        plt.plot(rx[group_labels], ry[group_labels], 'o', markersize=1, color=colors[i], label=i)

    plt.xlabel('x')
    plt.ylabel('y')
    plt.legend()
    plt.show()


if __name__ == '__main__':
    main()
    # mnist = input_data.read_data_sets('MNIST_data', one_hot=True)
    # b = mnist.train.next_batch(4)[0][0]
    # res = encoder(b)
    # s = decoder(res)
    # print(res.shape)