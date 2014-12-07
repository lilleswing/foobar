import math

__author__ = 'leswing'

memoize = {}
def score_half(lower, higher, num_to_see):
    """
    lower is the number of elements that would never be seen
    higher is the number of elements that would be seen
    num_seen is the number elements to be seen
    """
    if num_to_see > higher:
        return 0
    if num_to_see == 0 and higher > 0:
        return 0
    if higher == 0 and num_to_see == 0:
        return math.factorial(lower)
    if (lower, higher, num_to_see) in memoize:
        return memoize[(lower, higher, num_to_see)]

    total = 0
    if lower > 0: # put a rabbit that won't be seen
        total += score_half(lower - 1, higher, num_to_see) * lower
    # go through all partitions of higher
    for i in xrange(0, higher):
        n_lower = lower + i
        n_higher = higher - 1 - i
        partial = score_half(n_lower, n_higher, num_to_see - 1)
        total += partial
    memoize[lower, higher, num_to_see] = total
    return total

def get_side(x, n):
    if x > n:
        return 0
    if x == n:
        return 1
    if x == 0:
        return 0
    return score_half(0, n, x)


def n_choose_k(n, k):
    if 0 <= k <= n:
        ntok = 1
        ktok = 1
        for t in xrange(1, min(k, n - k) + 1):
            ntok *= n
            ktok *= t
            n -= 1
        answer = long(ntok // ktok)
        return answer
    else:
        return 0L


def answer_helper(x, y, n):
    total = 0
    for i in xrange(0, n):  # Pull out the tallest person try him everywhere
        left_list_size = i
        right_list_size = n - 1 - i
        combs_left = get_side(x - 1, left_list_size)
        combs_right = get_side(y - 1, right_list_size)
        partial = n_choose_k(n - 1, left_list_size) * combs_left * combs_right
        total += partial
    return total


def answer(x, y, n):
    return answer_helper(x, y, n)


