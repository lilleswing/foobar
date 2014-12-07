from fractions import gcd
# BOOOOOOOOOO computational geometry so
# Lots of edge cases

# 3 cases
# 1 co-horizontal and co-vertical
# a co-horizontal or a co-vertical
# neigher co-horizontal or co-vertical

def flip_horizontal(vertices):
    for i in xrange(0, len(vertices)):
        vertices[i][0] *= -1

def flip_vertical(vertices):
    for i in xrange(0, len(vertices)):
        vertices[i][1] *= -1

def flip_axis(vertices):
    for i in xrange(0, len(vertices)):
        vertices[i][0], vertices[i][1] = vertices[i][1], vertices[i][0]

def shift(vertices, x, y):
    for i in xrange(len(vertices)):
        vertices[i][0] += x
        vertices[i][1] -= y


def case1(vertices, minx, maxx, miny, maxy):
    j = maxx - minx
    k = maxy - miny
    for i in xrange(len(vertices)):
        if vertices[i][0] == minx and vertices[i][1] == miny:
            corner_index = i

    hy_indexes = range(3)
    hy_indexes.remove(corner_index)
    p1 = vertices[hy_indexes[0]]
    p2 = vertices[hy_indexes[1]]

    dx = abs(p1[0] - p2[0])
    dy = abs(p1[1] - p2[1])
    h = gcd(dx,dy) - 1

    return ((j -1) * (k - 1) - h) / 2


def case2(vertices, minx, maxx, miny, maxy):
    """
    two points exist on the minx line
    one point exists on the maxx line
    """
    j = maxx - minx
    k = maxy - miny

    corner_point = filter(lambda x: x[0] != minx, vertices)[0]
    left_points = filter(lambda x: x[0] == minx, vertices)
    left1 = left_points[0]
    left2 = left_points[1]
    b = abs(left1[1] - left2[1])

    dx1 = abs(corner_point[0] - left1[0])
    dy1 = abs(corner_point[1] - left1[1])
    h1 = gcd(dx1, dy1) - 1

    dx2 = abs(corner_point[0] - left2[0])
    dy2 = abs(corner_point[1] - left2[1])
    h2 = gcd(dx2, dy2) - 1

    i = (j - 1) * (k - 1) - h1 - h2
    i -= ((j - 1) * (k - 1) - h1) / 2
    i -= ((j - 1) * (k - b - 1) - h2) / 2

    return i

def get_corner_point(vertices, minx, maxx, miny, maxy):
    for point in vertices:
        corner_x = point[0] == minx or point[0] == maxx
        corner_y = point[1] == miny or point[1] == maxy
        is_corner_point = corner_x and corner_y
        if is_corner_point:
            corner_point = point
    if corner_point[0] == minx: # flip across y access
        flip_horizontal(vertices)
        minx, maxx = -1 * maxx, -1 * minx
    if corner_point[1] == miny: # flip across x access
        flip_vertical(vertices)
        miny, maxy = -1 * maxy, -1 * miny


def case3(vertices, minx, maxx, miny, maxy):
    corner_point =


def answer(vertices):
    # Step 1 -- create a bounding rectangle
    minx = min([x[0] for x in vertices])
    maxx = max([x[0] for x in vertices])

    miny = min([x[1] for x in vertices])
    maxy = max([x[1] for x in vertices])

    # see how many points are on each line
    co_vertical = False
    num_minx = len(filter(lambda x: x[0] == minx, vertices))
    num_maxx = len(filter(lambda x: x[0] == maxx, vertices))
    if num_minx == 2:
        co_vertical = True
    if num_maxx == 2:
        co_vertical = True
        flip_horizontal(vertices) # always co_horizontal on the left
        minx, maxx = -1 * maxx, -1 * minx

    co_horizontal = False
    num_miny = len(filter(lambda x: x[1] == miny, vertices))
    num_maxy = len(filter(lambda x: x[1] == maxy, vertices))
    if num_miny == 2:
        co_horizontal = True
    if num_maxy == 2: # always co_horizontal on bottom
        co_horizontal = True
        flip_vertical(vertices)
        miny, maxy = -1 * maxy, -1 * miny

    if co_horizontal and not co_vertical:
        flip_axis(vertices)
        miny, minx = minx, miny
        maxx, maxy = maxy, maxx

    if co_horizontal and co_vertical:
        answer = case1(vertices, minx, maxx, miny, maxy)
    elif co_horizontal ^ co_vertical:
        answer = case2(vertices, minx, maxx, miny, maxy)
    else:
        answer = case3(vertices, minx, maxx, miny, maxy)
    return "%d" % answer

def test_answer():
    t1 =[[0,0],[0,4],[8,0]]
    run_test(t1, 9)
    t2 =[[2,0],[0,4],[6,0]]
    run_test(t2, 5)


def run_test(t1, answer):
    import random
    check_answer(t1, answer)

    shift(t1, -7, 42)
    check_answer(t1, answer)

    random.shuffle(t1)
    check_answer(t1, answer)

    flip_vertical(t1)
    check_answer(t1, answer)

    flip_horizontal(t1)
    check_answer(t1, answer)

def check_answer(t, a):
    a1 = int(answer(t))
    if a1 != a:
        print "Wrong %s, %d" % (t, a1)
