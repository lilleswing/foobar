import copy
from itertools import product


def get_paths(subway):
    for i in xrange(1, len(subway) + 1):
        for path in product(range(len(subway[0])), repeat=i):
            yield path


def follow_path(path, subway, train):
    for turn in path:
        next_train = subway[train][turn]
        train = next_train
    return train


def is_meeting_path(path, subway):
    target = None
    for train in xrange(len(subway)):
        destination = follow_path(path, subway, train)
        if target is None:
            target = destination
        if target != destination:
            return False
    return True


def remove(subway, train):
    new_subway = copy.deepcopy(subway)
    for my_train in xrange(len(subway)):
        for turn in xrange(len(subway[0])):
            if new_subway[my_train][turn] == train:
                new_subway[my_train][turn] = subway[train][turn]
            if new_subway[my_train][turn] > train:
                new_subway[my_train][turn] -= 1
    new_subway.pop(train)
    return new_subway


def answer(subway):
    for path in get_paths(subway):
        if is_meeting_path(path, subway):
            return -1
    for train in xrange(len(subway)):
        altered_subway = remove(subway, train)
        for path in get_paths(altered_subway):
            if is_meeting_path(path, altered_subway):
                return train
    return -2


print(answer([[2, 1], [2, 0], [3, 1], [1, 0]]))
print(answer([[1, 2], [1, 1], [2, 2]]))
