__author__ = 'leswing'

# I didn't want to implement Gaussian Elimination in GF(2)
# But turned out it was harder to find a solution then to make one :(
# Timeout

def is_bit_set(value, bit_location):
    and_value = 1 << bit_location
    if value & and_value > 0:
        return True
    return False


def clear_bit(row_to_clear, clear_with, bit_location):
    if is_bit_set(row_to_clear, bit_location):
        return row_to_clear ^ clear_with
    return row_to_clear


def set_bit(row_index, xor, bit_location):
    row = xor[row_index]
    if is_bit_set(row, bit_location):
        return True
    for i in xrange(row_index + 1, len(xor)):
        this_row = xor[i]
        if is_bit_set(this_row, bit_location):
            xor[row_index] = xor[row_index] ^ xor[i]
            return True
    return False


def clear_lower(row_index, xor, bit_location):
    me = xor[row_index]
    for i in xrange(row_index + 1, len(xor)):
        clear_bit(xor[i], me, bit_location)


def gauss_jordan(xor, size):
    """
    NOTE(LESWING) the left-most element of the matrix in a row
    is the highest bit set (size -1), but we
    """
    for i in xrange(0, size):
        bit_location = size - i
        if not set_bit(i, xor, bit_location):
            return False
        clear_lower(i, xor, bit_location)

    # We now have a lower triangular matrix

    for row_index in xrange(0, size):
        for col_index in xrange(row_index+1, size):
            bit_location = size - col_index
            clear_bit(xor[row_index], xor[col_index], bit_location)
    return True


def flip(m, index):
    size = len(m)
    row = index // size
    col = index % size
    for i in xrange(size):
        m[row][i] += 1
        m[i][col] += 1
    m[row][col] += 1


def valid(m):
    for row in m:
        for value in row:
            if value % 2 != 0:
                return False
    return True


def answer(matrix):
    size = len(matrix)
    row_indexes = list()
    col_indexes = list()
    for i in xrange(size):
        row_part = list()
        col_part = list()
        for j in xrange(size):
            row_part.append(i * size + j)
            col_part.append(j * size + i)
        row_indexes.append(row_part)
        col_indexes.append(col_part)

    mp = list()
    row_size = size * size
    for i in xrange(size):
        for j in xrange(size):
            mp_row = [0] * row_size
            my_switches = set()
            my_switches.update(row_indexes[i])
            my_switches.update(col_indexes[j])
            for index in xrange(len(mp_row)):
                if index in my_switches:
                    mp_row[index] = 1
            mp_row.append(matrix[i][j])
            mp.append(mp_row)
    xor = list()
    for row in mp:
        s = "".join([str(x) for x in row])
        xor.append(int(s, 2))
    gauss_jordan(xor, len(matrix))
    total = 0
    for i in xrange(len(xor)):
        row = xor[i]
        val = row & 1
        if val == 1:
            flip(matrix, i)
        total += val
    if valid(matrix):
        return total
    return - 1


def test(m, a):
    #m = [[1, 1, 1, 0], [1, 1, 0, 1], [1, 0, 1, 1], [0, 1, 1, 1]]
    #on = [1, 1, 0, 0]
    #for i in xrange(len(m)):
    #    row = m[i]
    #    row.append(on[i])
    #print(gauss_jordan(m))
    #print(m)
    a1 = answer(m)
    if a1 != a:
        print("WRONG %s %d %d" % (m, a1, a))


test([[1, 1], [0, 0]], 2)
#test([[1, 1, 1], [1, 0, 0], [1, 0, 1]], -1)

