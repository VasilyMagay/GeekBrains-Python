# Отсортируйте по возрастанию методом слияния одномерный вещественный массив, заданный случайными числами
# на промежутке [0; 50). Выведите на экран исходный и отсортированный массивы.

import random


def merge_sort(array):
    def _merge(array1, array2):
        res = []
        i = 0
        j = 0
        while True:
            if array1[i] <= array2[j]:
                res.append(array1[i])
                i += 1
            else:
                res.append(array2[j])
                j += 1
            if i == len(array1) or j == len(array2):
                # добавляем оставшиеся элементы
                for k in range(i, len(array1)):
                    res.append(array1[k])
                for k in range(j, len(array2)):
                    res.append(array2[k])
                break

        return res

    if len(array) == 1:
        return array
    ind = len(array) // 2
    return _merge(merge_sort(array[0:ind]), merge_sort(array[ind:len(array)]))


SIZE = 10
my_array = [random.random() * 50 for i in range(SIZE)]
print(my_array)

print(merge_sort(my_array))
