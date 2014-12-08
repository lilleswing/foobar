__author__ = 'leswing'

# I didn't want to implement Gaussian Elimination in GF(2)
# But turned out it was harder to find a solution then to make one :(
# Timeout

def gauss_jordan(m, eps = 1.0/(10**10)):
    """Puts given matrix (2D array) into the Reduced Row Echelon Form.
       Returns True if successful, False if 'm' is singular.
       Specifically designed to minimize float roundoff.
       NOTE: make sure all the matrix items support fractions!
             An int matrix will NOT work!
       Written by Jarno Elonen in April 2005, released into Public Domain"""
    (h, w) = (len(m), len(m[0]))
    for y in range(0,h):
        maxrow = y
        for y2 in range(y+1, h):    # Find max pivot
            if abs(m[y2][y]) > abs(m[maxrow][y]):
                maxrow = y2
        (m[y], m[maxrow]) = (m[maxrow], m[y])
        if abs(m[y][y]) <= eps:     # Singular?
            return False
        for y2 in range(y+1, h):    # Eliminate column y
            c = m[y2][y] / m[y][y]
            for x in range(y, w):
                m[y2][x] -= m[y][x] * c
    for y in range(h-1, 0-1, -1): # Backsubstitute
        c  = m[y][y]
        for y2 in range(0,y):
            for x in range(w-1, y-1, -1):
                m[y2][x] -=  m[y][x] * m[y2][y] / c
        m[y][y] /= c
        for x in range(h, w):       # Normalize row y
            m[y][x] /= c
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
    gauss_jordan(mp)
    total = 0
    for i in xrange(len(mp)):
        row = mp[i]
        val = abs(row[-1]) % 2
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

