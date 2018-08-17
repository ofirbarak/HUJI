import ex2
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D

def gradDescent(S, LS):
    fig = plt.figure(figsize=(12,8))
    ax1 = fig.add_subplot(121)
    ax2 = fig.add_subplot(122,  projection='3d')

    cax1 = ax1.imshow(LS, extent=(-3,3,-3,3), origin='lower')
    ax1.set_xlabel('$w_1$')
    ax1.set_ylabel('$w_2$')
    fig.colorbar(cax1,ax=ax1)

    # draw gradients
    n_steps = 100
    alpha = 0.1
    fig.hold(True)
    w_cur = np.array([2.5,2.7])

    for i in range(n_steps):
        # w_last = w_cur
        g = ex2.calcGradient(S,w_cur)
        ax1.arrow(w_cur[0],w_cur[1],-alpha*g[0],-alpha*g[1],head_width=0.05, head_length=0.1,fc='k',ec='k')
        w_cur -= alpha*g

    ax2.set_xlabel('$x_1$')
    ax2.set_ylabel('$x_2$')
    ax2.set_zlabel('$y$')
    ax2.scatter(S[:,0], S[:,1], S[:,2])

    plt.show()
