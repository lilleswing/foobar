__author__ = 'leswing'
def least_bit_set(x):
    return x & (-x)


def delete_zeros_from(values, start):
    i = start
    for j in range(start, len(values)):
        if values[j] != 0:
            values[i] = values[j]
            i += 1
    del values[i:]


def eliminate(values):
    values = list(values)
    i = 0
    while True:
        delete_zeros_from(values, i)
        if i >= len(values):
            return values
        j = i
        for k in range(i + 1, len(values)):
            if least_bit_set(values[k]) < least_bit_set(values[j]):
                j = k
        values[i], values[j] = (values[j], values[i])
        for k in range(i + 1, len(values)):
            if least_bit_set(values[k]) == least_bit_set(values[i]):
                values[k] ^= values[i]
        i += 1


def in_span(x, eliminated_values):
    for y in eliminated_values:
        if least_bit_set(y) & x != 0:
            x ^= y
    return x == 0


def main():
    values = [1, 5, 8, 2, 10]
    eliminated_values = eliminate(values)
    print(eliminated_values)
    x = int(input())
    print(in_span(x, eliminated_values))


if __name__ == '__main__':
    main()