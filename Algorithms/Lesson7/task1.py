# Отсортируйте по убыванию методом пузырька одномерный целочисленный массив, заданный случайными числами
# на промежутке [-100; 100). Выведите на экран исходный и отсортированный массивы.
# Примечания:
# ● алгоритм сортировки должен быть в виде функции, которая принимает на вход массив данных,
# ● постарайтесь сделать алгоритм умнее, но помните, что у вас должна остаться сортировка пузырьком.
# Улучшенные версии сортировки, например, расчёской, шейкерная и другие в зачёт не идут.

import random


def bubble_sort(array):
    for j in range(1, len(array) - 1):
        for i in range(len(array) - j):
            if array[i] < array[i + 1]:
                array[i], array[i + 1] = array[i + 1], array[i]


SIZE = 10
my_array = [random.randint(-100, 99) for i in range(SIZE)]
print(my_array)

bubble_sort(my_array)
print(my_array)