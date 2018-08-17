import numpy as np


def sample(m, epsilon):
    matrix = np.zeros((m, 3))
    omega_star = np.asarray([0.6, -1])
    for i in range(m):
        x1 = matrix[i, 0] = np.random.uniform(0, 1)
        x2 = matrix[i, 1] = np.random.uniform(0, 1)
        x = np.asarray([x1, x2])
        matrix[i, 2] = np.inner(omega_star, x) + \
                       np.random.normal(0, epsilon)
    return matrix


def calcLS(S):
    w_low = -3
    w_up = 3
    mesh_range = np.arange(w_low, w_up, (w_up - w_low) / 200)
    ws = np.meshgrid(mesh_range, mesh_range)
    L_S = np.zeros((200, 200))
    m = S.shape[0]
    for i in range(200):
        for j in range(200):
            w = (ws[0][i, j], ws[1][i, j])
            sum = 0
            for k in range(m):
                x = np.asarray([S[k,0], S[k, 1]])
                y = S[k,2]
                sum += 0.5*(np.inner(w, x) - y)**2
            L_S[i, j] = 1/m*sum
    return L_S


def calcGradient(S, w):
    m = S.shape[0]
    g1 = 0
    g2 = 0
    for i in range(m):
        g1 += 0.5*(2*S[i,0]**2*w[0]+2*S[i,1]*S[i,0]*w[1]-2*S[i,0]*S[i,2])
    g1 /= m
    for i in range(m):
        g2 += 0.5*(2*S[i,1]**2*w[1]+2*S[i,0]*S[i,1]*w[0]-2*S[i,1]*S[i,2])
    g2 /= m
    return np.asarray([g1,g2])


"""
if __name__ == '__main__':
    import gradDescent as gd
    S_5_1 = sample(5, 1)
    LS5 = calcLS(S_5_1)
    gd.gradDescent(S_5_1, LS5)
    S_1000_01 = sample(1000, 0.001)
    LS1000 = calcLS(S_1000_01)
    gd.gradDescent(S_1000_01, LS1000)
"""