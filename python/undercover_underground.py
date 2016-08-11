# http://math.stackexchange.com/questions/689526/how-many-connected-graphs-over-v-vertices-and-e-edges

# NOTE(LESWING) these numbers get really big so be careful about the types
# And don't let them become floats or else you will get precision
# errors

memoize = dict()
bin_memoize = dict()


def n_choose_k(n, k):
    if (n, k) in bin_memoize:
        return bin_memoize[(n, k)]
    if 0 <= k <= n:
        ntok = 1
        ktok = 1
        for t in xrange(1, min(k, n - k) + 1):
            ntok *= n
            ktok *= t
            n -= 1
        binomial = long(ntok // ktok)
        bin_memoize[(n, k)] = binomial
        return binomial
    else:
        return 0L


def get_second(n, k):
    total = 0L
    for m in xrange(0, n - 1):
        coeff = n_choose_k(n - 1, m)
        total2 = 0L
        for p in xrange(0, k + 1):
            coeff2 = n_choose_k(((n - 1 - m) * (n - 2 - m)) / 2, p)
            value = q(m + 1, k - p)
            total2 += coeff2 * value
        total += coeff * total2
    return total


def q(n, k):
    if k < n - 1 or k > (n * (n - 1)) // 2:
        return 0L
    if (n, k) in memoize:
        return memoize[(n, k)]
    if k == n - 1:
        answer = long(n ** (n - 2))
        memoize[(n, k)] = answer
        return answer

    first = n_choose_k((n * (n - 1)) // 2, k)
    second = get_second(n, k)

    answer = long(first - second)
    memoize[(n, k)] = answer
    return answer


def answer(N, K):
    return "%d" % q(N, K)

# for n in xrange(2, 21):
#    for k in xrange(n-1, (n * (n - 1)) // 2 + 1):
#        answer(n,k)

print(answer(20, 150))
