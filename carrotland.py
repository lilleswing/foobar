from fractions import gcd
# BOOOOOOOOOO computational geometry so
# Lots of edge cases
# Algorithm description
# http://stackoverflow.com/questions/1049409/how-many-integer-points-within-the-three-points-forming-a-triangle

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


def boundary_points(p0, p1):
    return gcd(abs(p0[0] - p1[0]), abs(p0[1] - p1[1]))


def area(v):
    ax = v[0][0]
    ay = v[0][1]
    bx = v[1][0]
    by = v[1][1]
    cx = v[2][0]
    cy = v[2][1]

    num = abs(ax * (by - cy) + bx * (cy - ay) + cx * (ay - by))
    return num / 2


def answer(vertices):
    # Step 1 -- create a bounding rectangle
    a = area(vertices)
    p0 = vertices[0]
    p1 = vertices[1]
    p2 = vertices[2]
    b = boundary_points(p0, p1) + boundary_points(p1, p2) + boundary_points(p2, p0)
    answer = a + 1 - (b / 2)
    return "%d" % answer


def test_answer():
    t1 = [[0, 0], [0, 4], [8, 0]]
    run_test(t1, 9)
    t2 = [[2, 0], [0, 4], [6, 0]]
    run_test(t2, 5)
    t3 = [[0, 1], [5, 0], [2, 5]]
    run_test(t3, 10)
    t4 = [[2, 3], [6, 9], [10, 160]]
    run_test(t4, 289)
    t5 = [[91207, 89566], [-88690, -83026], [67100, 47194]]
    run_test(t5, 1730960165)


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

test_answer()
