import numpy as np

arr = []
for i in range(1, 10):
    for y in range(i):
        arr.append(i)


def split(array):
    groups = []
    i = 0
    last_list = None
    while i < len(array):
        current = array[i]
        if last_list is None:
            last_list = [current]
        else:
            if last_list[0] == current:
                last_list.append(current)
            else:
                groups.append((last_list))
                last_list = [current]
        i += 1
    return groups


arr = np.array(arr)
print(arr)
print(split(arr))
