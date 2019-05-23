# Массив размером 2m + 1, где m — натуральное число, заполнен случайным образом. Найдите в массиве медиану.
# Медианой называется элемент ряда, делящий его на две равные части: в одной находятся элементы, которые не меньше
# медианы, в другой — не больше медианы.
# Примечание: задачу можно решить без сортировки исходного массива. Но если это слишком сложно, используйте метод
# сортировки, который не рассматривался на уроках (сортировка слиянием также недопустима).

import random


def array_median(array):
    ind_exclude = []
    m = len(array) // 2
    median = 0

    for k in range(m):
        min_val = None
        max_val = None
        ind_min = None
        ind_max = None
        for i in range(len(array)):
            if i in ind_exclude:
                continue
            if min_val is None or array[i] < min_val:
                ind_min = i
                min_val = array[i]
            if max_val is None or array[i] > max_val:
                ind_max = i
                max_val = array[i]

        # Запоминаем индексы, чтобы дальше их не обрабатывать
        ind_exclude.append(ind_min)
        ind_exclude.append(ind_max)

        # print(f'{k}: {my_array}, min {min_val}, max {max_val}')

    for i in range(len(my_array)):
        if i not in ind_exclude:
            median = array[i]
            break

    return median


m = int(input('Введите число m: '))
my_array = [random.randint(0, 100) for i in range(2 * m + 1)]
print(my_array)

check_array = sorted(my_array)
print(f'Медиана массива = {array_median(my_array)}, проверка: {check_array} ({check_array[m]})')
