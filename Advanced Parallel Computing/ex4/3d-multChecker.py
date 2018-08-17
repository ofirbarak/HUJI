import numpy as np
import sys
import os
K = 5

def main():
    BLOCK_SIZE = int(sys.argv[1]) * K
    a_mat = np.zeros([BLOCK_SIZE, BLOCK_SIZE])
    b_mat = np.zeros([BLOCK_SIZE, BLOCK_SIZE])
    output_mat = np.zeros([BLOCK_SIZE, BLOCK_SIZE])

    input_A_files = []
    input_B_files = []
    output_files = []
    for file in os.listdir("./IO3"):
        if file.startswith('input_A'):
            input_A_files.append(file)
        elif file.startswith('input_B'):
            input_B_files.append(file)
        else:
            output_files.append(file)

    input_A_files = sorted(input_A_files)
    input_B_files = sorted(input_B_files)
    output_files = sorted(output_files)

    # build input and output matrices
    for file in input_A_files:
        coords = file[len('input_A'):].split('_')[1:]
        base_row = K * int(coords[0])
        base_col = K * int(coords[1])

        lines = open("IO3/" + file).read().replace('\n', '').replace(' ', '').strip()
        values = lines.split(',')[:-1]
        for i in range(K):
            for j in range(K):
                a_mat[base_row + i][base_col + j] = float(values[i * K + j])

    for file in input_B_files:
        coords = file[len('input_B'):].split('_')[1:]
        base_row = K * int(coords[0])
        base_col = K * int(coords[1])

        lines = open("IO3/" + file).read().replace('\n', '').replace(' ', '').strip()
        values = lines.split(',')[:-1]
        for i in range(K):
            for j in range(K):
                b_mat[base_row + i][base_col + j] = float(values[i * K + j])

    for file in output_files:
        coords = file[len('output_'):].split('_')
        base_row = K * int(coords[0])
        base_col = K * int(coords[1])

        lines = open("IO3/" + file).read().replace('\n', '').replace(' ', '').strip()
        values = lines.split(',')[:-1]
        for i in range(K):
            for j in range(K):
                output_mat[base_row + i][base_col + j] = float(values[i * K + j])

    print(np.array_equal(np.matmul(a_mat,b_mat), output_mat))

if __name__ == "__main__":
    main()
