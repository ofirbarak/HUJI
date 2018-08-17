import numpy as np
import sys
import os


def main():
    BLOCK_SIZE = int(sys.argv[1]) * 5
    input_mat = np.empty([BLOCK_SIZE, BLOCK_SIZE])
    output_mat = np.empty([BLOCK_SIZE, BLOCK_SIZE])
    input_files = []
    output_files = []
    for file in os.listdir("./IO"):
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
        base_col = 5 * int(coords[1])

        lines = open("IO/" + file).read().replace('\n', '').replace(' ', '').strip()
        values = lines.split(',')[:-1]
        for i in range(5):
            for j in range(5):
                input_mat[base_row + i][base_col + j] = float(values[i * 5 + j])

    for file in output_files:
        coords = file[len('output_'):].split('_')
        base_row = 5 * int(coords[0])
        base_col = 5 * int(coords[1])

        lines = open("IO/" + file).read().replace('\n', '').replace(' ', '').strip()
        values = lines.split(',')[:-1]
        for i in range(5):
            for j in range(5):
                output_mat[base_row + i][base_col + j] = float(values[i * 5 + j])

    print(np.array_equal(input_mat.T, output_mat))

if __name__ == "__main__":
    main()
