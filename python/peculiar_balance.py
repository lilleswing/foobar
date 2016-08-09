MAX = 1000000000


def ternary(n):
    if n == 0:
        return '0'
    nums = []
    while n:
        n, r = divmod(n, 3)
        nums.append(str(r))
    return ''.join(reversed(nums))


def answer(x):
    tern = ternary(x)
    tern = tern[::-1] + "0"

    result = list()
    carry = 0
    for n in tern:
        n = int(n)
        val = carry + n
        if val == 0:
            result.append("-")
            carry = 0
        elif val == 1:
            result.append("R")
            carry = 0
        elif val == 2:
            result.append("L")
            carry = 1
        elif val == 3:
            result.append("-")
            carry = 1

    if result[-1] == '-':
        result = result[:-1]
    return result


print answer(1000000000)
print answer(8)
print(answer(546))
assert (answer(2) == ["L", "R"])
assert (answer(8) == ["L", "-", "R"])

# 7 =  [1, 9] [3]
