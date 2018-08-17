

import matplotlib.pyplot as plt

def plotFromFile(fname):
    x = []
    y = []
    with open(fname) as f:
        for line in f:
            a, b = line.split(',')
            x.append(a)
            y.append(b)
    return x,y

def main():
    x,y = plotFromFile("/home/ofir/Desktop/results.txt")
    plt.plot(x,y, '-', label='6 nested loop')
    x,y = plotFromFile("/home/ofir/Desktop/3NestedLoopResults.txt")
    plt.plot(x, y, '-', label='3 nested loop')
    x, y = plotFromFile("/home/ofir/Desktop/RecursiveResults.txt")
    plt.plot(x, y, '-', label='recursive')
    plt.plot(x, [0.00319566]*len(x), '-', label="reported machine peak")
    plt.plot(x, [0.006990507]*len(x), '-', label="actual machine peak")
    plt.ylabel("Running time in sec")
    plt.xlabel("Block size")
    plt.title("Matrix size is 256x256")
    plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3,
               ncol=2, mode="expand", borderaxespad=0.)
    plt.show()


main()