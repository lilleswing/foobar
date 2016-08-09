def create_dp_grid(grid):
    dp = []
    for i in xrange(len(grid)):
        row = [set()] * len(grid[0])
        dp.append(row)
    return dp


def get_possible_foods(dp, i, j):
    food_bag_sizes = set()
    if i - 1 >= 0:
        food_bag_sizes.update(dp[i - 1][j])
    if j - 1 >= 0:
        food_bag_sizes.update(dp[i][j - 1])
    return food_bag_sizes


def answer(food, grid):
    dp = create_dp_grid(grid)
    dp[0][0] = {food}
    for i in xrange(0, len(grid)):
        for j in xrange(len(grid[0])):
            if i == 0 and j == 0:
                continue
            zombie_hunger = grid[i][j]
            possible_foods = get_possible_foods(dp, i, j)
            new_foods = [x - zombie_hunger for x in possible_foods]
            new_foods = filter(lambda x: x >= 0, new_foods)
            dp[i][j] = set(new_foods)
    food_possible = dp[-1][-1]
    if len(food_possible) == 0:
        return -1
    return min(food_possible)


print(answer(7, [[0, 2, 5], [1, 1, 3], [2, 1, 1]]))
print(answer(12, [[0, 2, 5], [1, 1, 3], [2, 1, 1]]))
