def swap(matrix, row, zero_column, equation_matrix):
    count = 1
    switch_row = matrix[row].copy()
    row_equation = equation_matrix[row]
    while row + count <= len(matrix) - 1 and matrix[row][zero_column] == 0:
        if matrix[row + count][zero_column] == 0:
            count += 1
            continue
        next_row = matrix[row + count].copy()
        next_row_equation = equation_matrix[row + count]
        matrix[row] = next_row
        equation_matrix[row] = next_row_equation
        matrix[row + count] = switch_row
        equation_matrix[row + count] = row_equation
    return [matrix, equation_matrix]


def sort_matrix(matrix, equation_matrix):
    matrix_clone = matrix.copy()
    equation_matrix_clone = equation_matrix.copy()
    matrix_width = len(matrix_clone[0]) - 1
    for column in range(0, matrix_width + 1):
        for row, item in enumerate(matrix):
            [matrix_clone, equation_matrix_clone] = swap(matrix_clone, row, matrix_width - column, equation_matrix)
    return [matrix_clone, equation_matrix_clone]


def sort_for_echelon(matrix, equation_matrix):
    [matrix, equation_matrix] = sort_matrix(matrix, equation_matrix)
    return sort_matrix(matrix, equation_matrix)


def multiply_row(row, by):
    clone_matrix = row.copy()
    for i, item in enumerate(clone_matrix):
        clone_matrix[i] = item * by
    return clone_matrix


def add_row_multiply(row1, row2):
    if len(row1) != len(row2):
        return False
    for i, item in enumerate(row1):
        row1[i] = row2[i] - item
    return row1


def get_echelon_form(augmented_matrix):
    matrix_clone = augmented_matrix.copy()
    equation_matrix = matrix_clone.pop(len(matrix_clone) - 1)
    if len(matrix_clone) != len(equation_matrix):
        print("invalid matrix")
        return
    [coefficient, equation_matrix] = sort_for_echelon(matrix_clone, equation_matrix)
    print("coefficient, ==", coefficient)
    print("equation_matrix, ==", equation_matrix)
    width = len(coefficient[0])
    height = len(coefficient)
    #  to make working easier
    coefficient.reverse()
    equation_matrix.reverse()
    first_non_zero_index_pos = width - 1
    for column in range(0, width):
        for row in range(0, height):
            if row >= height - 1:  # to skip the last row
                continue
            if row >= first_non_zero_index_pos:
                break
            first = coefficient[row][column]
            second = coefficient[row + 1][column]
            if first == 0 or second == 0:
                coefficient.reverse()
                equation_matrix.reverse()
                [coefficient, equation_matrix] = sort_for_echelon(coefficient, equation_matrix)
                coefficient.reverse()
                equation_matrix.reverse()
                first = coefficient[row][column]
                second = coefficient[row + 1][column]
            coefficient[row] = add_row_multiply(multiply_row(coefficient[row + 1], first),
                                                multiply_row(coefficient[row], second))
            equation_matrix[row] = (first * equation_matrix[row - 1]) - (second * equation_matrix[row])
        first_non_zero_index_pos -= 1
    coefficient.reverse()
    echelon_matrix = coefficient.copy()
    # combine equation matrix and augmented matrix
    echelon_matrix.append(equation_matrix)
    return echelon_matrix


def validate_matrix(matrix: list[list[int]]):
    for i, row in enumerate(matrix):
        if len(matrix[i - 1]) != len(row):
            print("Invalid Matrix")
            return []
    return matrix


class Matrix:
    matrix: list[list[int]] = []
    order = (0, 0)

    def __int__(self, matrix: list[list[int]]):
        self.matrix = validate_matrix(matrix)
        order = (len(self.matrix), len(self.matrix[0]))


# arr = [[0,1,0], [6,9,0], [2,6,1], [2,0,3]]
# arr = [[2,3,1], [6,9,3], [4,6,2], [2,0,3]]
# arr = [[1,2,3], [4,5,6], [7,8,9], [2,1,1]]
arr = [[1, 2, 3, 4], [0, 0, 0, 9], [0, 4, 5, 6], [0, 0, 1, 0], [2, 1, 1, 0]]
# arr = [[1,1,2], [2,4,-3], [3,6,-5], [0,0,0]]
# arr = [[1,1,0], [0,0,-3], [3,6,-5], [3,6,-5], [0,6,0, 1]]
# arr = [[1,-1,2], [2,0,2], [1,-3,4], [2,-1,2]]
# arr = [[1,2,-3, 2], [2,5,-8,6],  [3,4,-5,2],  [2,5,4]]
# arr = [[0,2,1], [1,-1,1],  [4,-4,4],  [0,0,0]]
# arr = [[-1,2,1], [1,-2,1],  [4,-4,3],  [0,0,0]]
