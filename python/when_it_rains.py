def answer(heights):
    if len(heights) <= 2:
        return 0
    max_left = [0] * len(heights)
    max_left[0] = heights[0]
    for i in xrange(1, len(heights)):
        max_left[i] = max(max_left[i-1], heights[i])

    max_right = [0] * len(heights)
    max_right[-1] = heights[-1]
    for i in xrange(len(heights)-2, -1, -1):
        max_right[i] = max(max_right[i+1], heights[i])

    total = 0
    for i in xrange(1, len(heights)-1):
        left = max_left[i]
        me = heights[i]
        right = max_right[i]
        water_height = min(left, right)
        total += water_height - me
    return total
