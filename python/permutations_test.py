import math

__author__ = 'leswing'
import line_up_the_captives


def permutations(iterable, r=None):
# permutations('ABCD', 2) --> AB AC AD BA BC BD CA CB CD DA DB DC
# permutations(range(3)) --> 012 021 102 120 201 210
    pool = tuple(iterable)
    n = len(pool)
    r = n if r is None else r
    if r > n:
        return
    indices = range(n)
    cycles = range(n, n - r, -1)
    yield tuple(pool[i] for i in indices[:r])
    while n:
        for i in reversed(range(r)):
            cycles[i] -= 1
            if cycles[i] == 0:
                indices[i:] = indices[i + 1:] + indices[i:i + 1]
                cycles[i] = n - i
            else:
                j = cycles[i]
                indices[i], indices[-j] = indices[-j], indices[i]
                yield tuple(pool[i] for i in indices[:r])
                break
        else:
            return


def count_rabbits(y, l):
    biggest = float('-inf')
    total = 0
    for elem in l:
        if elem > biggest:
            total += 1
            biggest = elem
    return total

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



def exhaust_answer(x, y, n):
    correct = 0
    for perm in permutations(range(n)):
        count_forward = count_rabbits(x, perm)
        count_backward = count_rabbits(y, perm[::-1])
        if count_forward == x and count_backward == y:
            #print(perm, count_forward, count_backward)
            correct += 1
    return correct

def main():
    n = 3
    while True:
        for x in xrange(1, n):
            for y in xrange(1, n):
                a1 = line_up_the_captives.answer_helper(x, y, n)
                a2 = exhaust_answer(x, y, n)
                if a1 != a2:
                    print(x, y, n)
        n += 1


if __name__ == "__main__":
    pass
    #main()


