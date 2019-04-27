# В массиве найти максимальный отрицательный элемент. Вывести на экран его значение и позицию в массиве.
# Примечание к задаче: пожалуйста не путайте «минимальный» и «максимальный отрицательный».
# Это два абсолютно разных значения.

import random

array = [random.randint(-100, 100) for _ in range(10)]
print(f'{array}')

pos = 0
max_negative = None
for i, num in enumerate(array):
    if num < 0:
        if not max_negative or num > max_negative:
            max_negative = num
            pos = i

print(f'Максимальный отрицательный элемент {max_negative} в позиции {pos + 1}'
      if max_negative else print('Нет отрицательных элементов в массиве'))
