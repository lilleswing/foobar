def answer(t, n):
    dp = [0] * n
    dp[0] = 1
    for np in xrange(t):
        # print(dp)
        next_row = [0] * n
        for i in xrange(n):
            for j in xrange(-1, 2):
                if j == 1 and i + j == len(dp) - 1:  # Not allowed to move out of end location
                    continue
                if 0 <= i + j < len(dp):
                    next_row[i] += dp[i + j]
        dp = next_row

    return dp[-1] % 123454321
