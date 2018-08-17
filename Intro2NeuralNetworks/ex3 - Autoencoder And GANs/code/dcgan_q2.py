import tensorflow as tf
import numpy as np

import matplotlib
#matplotlib.use('Agg')

from matplotlib import pyplot as plt
import matplotlib.gridspec as gridspec
import sys
import ModuleForQ2_version1
import random
import time
from tensorflow.examples.tutorials.mnist import input_data

ModuleForQ2_version1.main()

# Uniformly independently distributed random vectors z
UNIFORM_Z = 0

# Random vectors sampled from a Gaussian mixture distribution
GAUSSIAN_MIXTURE = 1

# latent representation of the autoencoder
AUTOENCODER = 2


# set to UNIFORM_Z / GAUSSIAN_MIXTURE / AUTOENCODER
CURRENT_METHOD = 1

INPUT = 28 * 28
mnist = input_data.read_data_sets('MNIST_data', one_hot=True)
MNIST_SIZE = mnist.train.images.shape[0]
BATCH_SIZE2 = 1000 #mnist batch iterate
LATENT_SIZE = 100

sess = None
za = None
bx = None


# def return_sampled_z():
#     random.seed(time.time)
#     i = random.randint(0, MNIST_SIZE)
#     batch_x = None
#     for j in range(0, i, BATCH_SIZE2):
#         batch_x, _ = mnist.train.next_batch(BATCH_SIZE2)
#
#     mnist_image = batch_x[i % BATCH_SIZE2].reshape(1,784)
#     # print(type(sess), type(zs))
#     return sess.run(zs, feed_dict={bx: mnist.train.images[0].reshape(1,784)})


def get_rand(batch_size):
    if CURRENT_METHOD == UNIFORM_Z:
        return np.random.uniform(-1., 1., size=[batch_size, 100])

    if CURRENT_METHOD == GAUSSIAN_MIXTURE:
        centers = [-0.1, -0.08, -0.06, -0.04, -0.02, 0, 0.02, 0.04, 0.06, 0.08, 0.1]
        # for each cell find a center with uniform distribution (there are 10 centers)
        random_centers = np.random.choice(centers, (batch_size, 100))
        # now each cell contains a center, sample with gausssian distribution around this center
        return np.random.normal(random_centers, 0.05)

    if CURRENT_METHOD == AUTOENCODER:
        return ModuleForQ2_version1.return_sampled_z(batch_size)
        # c = return_sampled_z(1)
        # print(c)
        # f = np.vectorize(return_sampled_z)
        # c =  np.fromfunction(return_sampled_z, (batch_size,))
        # print("#################################################", c.shape)
        # return c



def plot(samples, D_loss, G_loss, epoch, total):
    fig = plt.figure(figsize=(10, 5))

    gs = gridspec.GridSpec(4, 8)
    gs.update(wspace=0.05, hspace=0.05)

    # Plot losses
    ax = plt.subplot(gs[:, 4:])
    ax.plot(D_loss, label="discriminator's loss", color='b')
    ax.plot(G_loss, label="generator's loss", color='r')
    ax.set_xlim([0, total])
    ax.yaxis.tick_right()
    ax.legend()
    ax.set_ylim([0, 3])

    # Generate images
    for i, sample in enumerate(samples):

        if i > 4 * 4 - 1:
            break
        ax = plt.subplot(gs[i % 4, int(i / 4)])
        plt.axis('off')
        ax.set_xticklabels([])
        ax.set_yticklabels([])
        ax.set_aspect('equal')
        plt.imshow(sample.reshape(28, 28), cmap='Greys_r')

    plt.savefig('./output/' + str(epoch + 1) + '.png')
    plt.close()


def Conv2d(input, output_dim=64, kernel=(5, 5), strides=(2, 2), stddev=0.2, name='conv_2d'):
    with tf.variable_scope(name):
        W = tf.get_variable('Conv2dW', [kernel[0], kernel[1], input.get_shape()[-1], output_dim],
                            initializer=tf.truncated_normal_initializer(stddev=stddev))
        b = tf.get_variable('Conv2db', [output_dim], initializer=tf.zeros_initializer())

        return tf.nn.conv2d(input, W, strides=[1, strides[0], strides[1], 1], padding='SAME') + b


def Deconv2d(input, output_dim, batch_size, kernel=(5, 5), strides=(2, 2), stddev=0.2, name='deconv_2d'):
    with tf.variable_scope(name):
        W = tf.get_variable('Deconv2dW', [kernel[0], kernel[1], output_dim, input.get_shape()[-1]],
                            initializer=tf.truncated_normal_initializer(stddev=stddev))
        b = tf.get_variable('Deconv2db', [output_dim], initializer=tf.zeros_initializer())

        input_shape = input.get_shape().as_list()
        output_shape = [batch_size,
                        int(input_shape[1] * strides[0]),
                        int(input_shape[2] * strides[1]),
                        output_dim]

        deconv = tf.nn.conv2d_transpose(input, W, output_shape=output_shape,
                                        strides=[1, strides[0], strides[1], 1])

        return deconv + b


def Dense(input, output_dim, stddev=0.02, name='dense'):
    with tf.variable_scope(name):
        shape = input.get_shape()
        W = tf.get_variable('DenseW', [shape[1], output_dim], tf.float32,
                            tf.random_normal_initializer(stddev=stddev))
        b = tf.get_variable('Denseb', [output_dim],
                            initializer=tf.zeros_initializer())

        return tf.matmul(input, W) + b


def BatchNormalization(input, name='bn'):
    with tf.variable_scope(name):

        output_dim = input.get_shape()[-1]
        beta = tf.get_variable('BnBeta', [output_dim],
                               initializer=tf.zeros_initializer())
        gamma = tf.get_variable('BnGamma', [output_dim],
                                initializer=tf.ones_initializer())

        if len(input.get_shape()) == 2:
            mean, var = tf.nn.moments(input, [0])
        else:
            mean, var = tf.nn.moments(input, [0, 1, 2])
        return tf.nn.batch_normalization(input, mean, var, beta, gamma, 1e-5)


def LeakyReLU(input, leak=0.2, name='lrelu'):
    return tf.maximum(input, leak * input)


BATCH_SIZE = 64
EPOCHS = 25


def Discriminator(X, reuse=False, name='d'):
    with tf.variable_scope(name, reuse=reuse):

        if len(X.get_shape()) > 2:
            # X: -1, 28, 28, 1
            D_conv1 = Conv2d(X, output_dim=64, name='D_conv1')
        else:
            D_reshaped = tf.reshape(X, [-1, 28, 28, 1])
            D_conv1 = Conv2d(D_reshaped, output_dim=64, name='D_conv1')
        D_bn1 = BatchNormalization(D_conv1, name='D_bn1')
        D_h1 = LeakyReLU(D_bn1)  # [-1, 28, 28, 64]
        D_conv2 = Conv2d(D_h1, output_dim=128, name='D_conv2')
        D_bn2 = BatchNormalization(D_conv2, name='D_bn2')
        D_h2 = LeakyReLU(D_bn2)  # [-1, 28, 28, 128]
        D_r2 = tf.reshape(D_h2, [-1, 6272])
        D_h3 = LeakyReLU(D_r2)  # [-1, 256]
        D_h4 = tf.nn.dropout(D_h3, 0.5)
        D_h5 = Dense(D_h4, output_dim=1, name='D_h5')  # [-1, 1]
        return tf.nn.sigmoid(D_h5)


def Generator(z, name='g'):
    with tf.variable_scope(name):
        G_1 = Dense(z, output_dim=1024, name='G_1')  # [-1, 1024]
        G_bn1 = BatchNormalization(G_1, name='G_bn1')
        G_h1 = tf.nn.relu(G_bn1)
        G_2 = Dense(G_h1, output_dim=7 * 7 * 128, name='G_2')  # [-1, 7*7*128]
        G_bn2 = BatchNormalization(G_2, name='G_bn2')
        G_h2 = tf.nn.relu(G_bn2)
        G_r2 = tf.reshape(G_h2, [-1, 7, 7, 128])
        G_conv3 = Deconv2d(G_r2, output_dim=64, batch_size=BATCH_SIZE, name='G_conv3')
        G_bn3 = BatchNormalization(G_conv3, name='G_bn3')
        G_h3 = tf.nn.relu(G_bn3)
        G_conv4 = Deconv2d(G_h3, output_dim=1, batch_size=BATCH_SIZE, name='G_conv4')
        G_r4 = tf.reshape(G_conv4, [-1, 784])
        return tf.nn.sigmoid(G_r4)


X = tf.placeholder(tf.float32, shape=[None, 784])
z = tf.placeholder(tf.float32, shape=[None, 100])

G = Generator(z, 'G')
D_real = Discriminator(X, False, 'D')
D_fake = Discriminator(G, True, 'D')

# D_loss = -tf.reduce_mean(tf.log(D_real) - tf.log(D_fake))  # Train to judge if the data is real correctly
D_loss = -tf.reduce_mean(tf.log(D_real)) - tf.reduce_mean(tf.log(1 - D_fake))
G_loss = -tf.reduce_mean(tf.log(D_fake))  # Train to pass the discriminator as real data

vars = tf.trainable_variables()
d_params = [v for v in vars if v.name.startswith('D/')]
g_params = [v for v in vars if v.name.startswith('G/')]

D_solver = tf.train.AdamOptimizer(learning_rate=1e-4, beta1=0.1).minimize(D_loss, var_list=d_params)
G_solver = tf.train.AdamOptimizer(learning_rate=2e-4, beta1=0.3).minimize(G_loss, var_list=g_params)


# # part B.c
# # Create the model
# bx = tf.placeholder(tf.float32, [None, INPUT])
#
# # Build the graph for the deep net
# zs = ModuleForQ2_version1.encoder(bx)
# output = ModuleForQ2_version1.decoder(zs)
#
# vars = tf.trainable_variables()
# e_params = [v for v in vars if v.name.startswith('encoder')]
#
# # Create a saver (for restoring the weights)
# saver = tf.train.Saver(e_params)


with tf.Session() as sess:
    ModuleForQ2_version1.main()
    sess.run(tf.global_variables_initializer())
    # restore values from encoder of q.1
    # saver.restore(sess, './savedModel/encoder.ckpt')


    D_loss_vals = []
    G_loss_vals = []

    iteration = int(mnist.train.images.shape[0] / BATCH_SIZE)
    for e in range(EPOCHS):
        for i in range(iteration):
            x, _ = mnist.train.next_batch(BATCH_SIZE)
            rand = get_rand(BATCH_SIZE)
            _, D_loss_curr = sess.run([D_solver, D_loss], {X: x, z: rand})
            rand = get_rand(BATCH_SIZE)
            _, G_loss_curr = sess.run([G_solver, G_loss], {z: rand})

            D_loss_vals.append(D_loss_curr)
            G_loss_vals.append(G_loss_curr)

            sys.stdout.write("\r%d / %d: %f, %f" % (i, iteration, D_loss_curr, G_loss_curr))
            sys.stdout.flush()

        data = sess.run(G, {z: rand})

        plot(data, D_loss_vals, G_loss_vals, e, EPOCHS * iteration)