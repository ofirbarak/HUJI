import numpy as np
import sys
import os
from scipy import ndimage, signal


def main():
    P = int(sys.argv[1])
    BLOCK_SIZE = P * 5
    input_mat = []
    output_mat = []
    input_files = []
    output_files = []
    for file in os.listdir("./IO2"):
        if file.startswith('input'):
            input_files.append(file)
        else:
            output_files.append(file)
    input_files = sorted(input_files)
    output_files = sorted(output_files)

    # build input and output matrices
    for file in input_files:
        coords = file[len('input_'):].split('_')
        base_row = 5 * int(coords[0])
        base_col = int(coords[1])

        lines = open("IO2/" + file).read().replace('\n', '').replace(' ', '').strip()
        values = lines.split(',')[:-1]
        input_mat.append([list(map(int, values))])

    input_mat = np.asarray(input_mat)
    input_mat = input_mat.reshape((P, P, 5))

    for file in output_files:
        coords = file[len('output_'):].split('_')
        base_row = 5 * int(coords[0])
        base_col = int(coords[1])

        lines = open("IO2/" + file).read().replace('\n', '').replace(' ', '').strip()
        values = lines.split(',')[:-1]
        output_mat.append([list(map(int, values))])

    output_mat = np.asarray(output_mat)
    output_mat = output_mat.reshape((P,P,5))

    kernel = np.array([[0,2,0],
                       [4,1,3],
                       [0,1,0]])

    calc_matrix = np.zeros((P,P,5))
    for i in range(5):
        calc_matrix[:,:,i] = signal.convolve2d(input_mat[:,:,i], kernel, boundary='wrap', mode='same')

    print(np.array_equal(calc_matrix, output_mat))

if __name__ == "__main__":
    main()
