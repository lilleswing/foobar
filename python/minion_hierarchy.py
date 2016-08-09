def answer(x):
    total = 1
    level = 1
    for i in xrange(x):
        level *= 7
        total += level
    return total

