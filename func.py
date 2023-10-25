import numpy as np
def determinant(matrix):
    if len(matrix) == 2 and len(matrix[0]) == 2:
        return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
    det = 0
    for c in range(len(matrix)):
        sub_matrix = [row[:c] + row[c + 1:] for row in matrix[1:]]
        sign = (-1) ** c
        det += sign * matrix[0][c] * determinant(sub_matrix)
        return det
matrix = [[1,2],[3,4]]
print(determinant(matrix))
print(np.linalg.matrix_rank(matrix))
print(np.linalg.inv(matrix))
