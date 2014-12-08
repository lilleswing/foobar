squares = [x * x for x in range(1,101)]

dp = list()
for i in xrange(0,10001):
    dp.append(float('inf'))

dp[0] = 0
for square in squares:
    dp[square] = 1

for i in xrange(2, 10001):
    best = dp[i]
    for square in squares:
        prev_index = i - square
        if prev_index < 0:
            break
        guess = dp[prev_index] + 1
        if guess < best:
            best = guess
    dp[i] = best

def answer(n):
    return dp[n]
