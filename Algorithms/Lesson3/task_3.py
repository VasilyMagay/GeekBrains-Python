# В массиве случайных целых чисел поменять местами минимальный и максимальный элементы.

import random

MAX_NUM = 100

array = [random.randint(0, MAX_NUM) for _ in range(10)]
print(f'{array}')

min_val = MAX_NUM + 1
min_pos = 0

max_val = 0
max_pos = 0

for i, num in enumerate(array):
    if num < min_val:
        min_val = num
        min_pos = i
    if num > max_val:
        max_val = num
        max_pos = i

array[min_pos], array[max_pos] = array[max_pos], array[min_pos]
print(f'{array}')
print(f'Min {min_val} at pos {min_pos + 1}')
print(f'Max {max_val} at pos {max_pos + 1}')
