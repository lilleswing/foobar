__author__ = 'leswing'


def answer(L, k):
    last = [-1 * float('inf')] * k
    now = [-1 * float('inf')] * k
    now[0] = L[0]

    best = -1 * float('inf')

    for i in xrange(1, len(L)):
        last, now = now, last
        now = [-1 * float('inf')] * k
        now[0] = L[i]
        for j in xrange(1, k):
            now[j] = max(last[j - 1] + L[i], now[j - 1])
            if now[j] > best:
                best = now[j]

    return best


def test(l, k, ans):
    a1 = answer(l, k)
    if a1 != ans:
        print "WRONG %s %s %d" % (l, k, a1)


test([-100, 95, 86, 47], 3, 228)
test([40, 91, -68, -36, 24, -67, -32 - 23, -33, -52], 7, 131)
