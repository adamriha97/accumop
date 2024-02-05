import numpy as np


matrix = np.ones((3, 3))

# Define padding size (number of rows and columns to add)
top_padding = 3
bottom_padding = 3
left_padding = 1
right_padding = 3

# Add padding to the matrix
padded_matrix = np.pad(matrix, ((top_padding, bottom_padding), (left_padding, right_padding)), mode='constant', constant_values=0)

print(padded_matrix)
print(matrix.shape)
print(matrix[0][0])
print(padded_matrix.shape)
print(padded_matrix[0][0])

'''
# create new matrix
        mx_new = np.zeros((const.MX_LONG, const.MX_LAT))
        for i in range(padding, x - padding, 1):
            print(i, 'of', x)
            for j in range(padding, y - padding, 1):
                for zi in range(dimension):
                    for zj in range(dimension):
                        k = i + zi - distance
                        l = j + zj - distance
                        ni = i - padding
                        nj = j - padding
                        mx_new[ni][nj] = mx_new[ni][nj] + padded_matrix[k][l] * kernel_matrix[zi][zj]
        mx_new = self.normalize_matrix(mx_new)
        return mx_new
'''