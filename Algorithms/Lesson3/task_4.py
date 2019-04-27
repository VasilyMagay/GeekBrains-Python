# Определить, какое число в массиве встречается чаще всего.

import random

array = [random.randint(0, 10) for _ in range(100)]
print(f'{array}')

result = {}
for num in array:
    if not result.get(num):
        result[num] = 0
    result[num] += 1

max_count = 0
max_num = 0
for num, dig in result.items():
    print(f'Число {num} встречается {dig} раз')
    if dig > max_count:
        max_count = dig
        max_num = num

print(f'\nЧисло {max_num} встречается чаще всего, {max_count} раз')
