import numpy
import matplotlib.pyplot as plt

data = numpy.random.binomial(1, 0.25, (100000, 1000))
epsilon = [0.5, 0.25, 0.1, 0.01, 0.001]
## B-1
X = numpy.zeros((1000, 1))
Y = [i for i in range(1000)]
for row in range(5):
    X[0, 0] = data[row, 0]
    for i in range(1,1000):
        X[i, 0] = numpy.sum(data[row, :i]) / i
    plt.plot(Y, X, label='row'+str(row+1))
plt.legend(loc='best')
plt.show()


## B-2
Chevishev = lambda x, y: 1 / (4 * x * y ** 2)
Hoffeding = lambda x, y: 2 * numpy.exp(-2 * x * y ** 2)
X = numpy.zeros((1000, 1))
Y = numpy.arange(1000)

##B-3
a = numpy.zeros((100000, 1), dtype=float)
data_expectation = numpy.copy(data)

for i in range(1, 1000):
    data_expectation[:, i] = data[:, i] + data_expectation[:, i - 1]

for eps in epsilon:
    for i in range(1, 1000):
        X[i, 0] = (Chevishev(i, eps))
    plt.plot(Y, X.clip(0, 1), label='Chebyshev', linewidth=0.4)
    for i in range(1, 1000):
        X[i, 0] = (Hoffeding(i, eps))
    plt.plot(Y, X.clip(0, 1), label='Hoeffding', linewidth=0.4)
    ###############C########################
    d = numpy.zeros(1000)
    for i in range(1, 1000):
        a = data_expectation[:,i]/i
        d[i] = numpy.count_nonzero((numpy.abs(a-0.25) >= eps), axis=0)
    plt.plot(Y, d / 100000, label='percentage', linewidth=0.4)
    plt.legend(loc='best')
    plt.title('epsilon=' + str(eps))
    plt.show()
