# Python 3.6.2 (v3.6.2:5fd33b5, Jul  8 2017, 04:57:36) [MSC v.1900 64 bit (AMD64)] on win32
# Windows 8.1 (64 bit)
import sys


def calc_size(x):
    result = sys.getsizeof(x)
    if hasattr(x, '__iter__'):
        if hasattr(x, 'items'):
            for key, value in x.items():
                result += calc_size(key) + calc_size(value)
        elif not isinstance(x, str):
            for item in x:
                result += calc_size(item)
    return result


def calc_total(mydict):
    result = 0
    for key, _ in mydict.items():
        c = calc_size(eval(key))
        print(f'\t{key} = {c}, type={type(eval(key))}')
        result += c
    return result


start_locals = locals().copy()

# Начало программы ****************************************************

#  Программа №1
# num = int(input('Введите целое трехзначное число: '))
#
# if 1000 > num >= 100:
#     hundreds = num // 100
#     decades = (num % 100) // 10
#     units = (num % 100) % 10
#
#     print(f'Сумма цифр: {hundreds + decades + units}')
#     print(f'Произведение цифр: {hundreds * decades * units}')
# **************************************************
# {'num': 159, 'hundreds': 1, 'decades': 5, 'units': 9}
# 	num = 28, type=<class 'int'>
# 	hundreds = 28, type=<class 'int'>
# 	decades = 28, type=<class 'int'>
# 	units = 28, type=<class 'int'>
# Переменные занимают: 112 байт

# Программа №2
# dig5 = 101
# dig6 = 110
#
# dig5_1 = dig5 // 100
# dig5_2 = (dig5 % 100) // 10
# dig5_3 = (dig5 % 100) % 10
#
# dig6_1 = dig6 // 100
# dig6_2 = (dig6 % 100) // 10
# dig6_3 = (dig6 % 100) % 10
#
# operation_and = f'{dig5_1 * dig6_1}{dig5_2 * dig6_2}{dig5_3 * dig6_3}'
# operation_or = f'{1 if (dig5_1 + dig6_1) > 0 else 0}{1 if (dig5_2 + dig6_2) > 0 else 0}{1 if (dig5_3 + dig6_3) > 0 else 0}'
# operation_not5 = f'{1 if dig5_1 == 0 else 0}{1 if dig5_2 == 0 else 0}{1 if dig5_3 == 0 else 0}'
# operation_not6 = f'{1 if dig6_1 == 0 else 0}{1 if dig6_2 == 0 else 0}{1 if dig6_3 == 0 else 0}'
#
# print(f'Операция "И" с числами {dig5} и {dig6}: {operation_and}')
# print(f'Операция "ИЛИ" с числами {dig5} и {dig6}: {operation_or}')
# print(f'Операция "НЕ" с числом {dig5}: {operation_not5}')
# print(f'Операция "НЕ" с числом {dig6}: {operation_not6}')
# print(f'Побитовый сдвиг числа {dig5} вправо на 2 знака: {dig5 // 100}')
# print(f'Побитовый сдвиг числа {dig5} влево на 2 знака: {dig5 * 100}')
# **************************************************
# {'dig5': 101, 'dig6': 110, 'dig5_1': 1, 'dig5_2': 0, 'dig5_3': 1, 'dig6_1': 1, 'dig6_2': 1, 'dig6_3': 0, 'operation_and': '100', 'operation_or': '111', 'operation_not5': '010', 'operation_not6': '001'}
# 	dig5 = 28, type=<class 'int'>
# 	dig6 = 28, type=<class 'int'>
# 	dig5_1 = 28, type=<class 'int'>
# 	dig5_2 = 24, type=<class 'int'>
# 	dig5_3 = 28, type=<class 'int'>
# 	dig6_1 = 28, type=<class 'int'>
# 	dig6_2 = 28, type=<class 'int'>
# 	dig6_3 = 24, type=<class 'int'>
# 	operation_and = 52, type=<class 'str'>
# 	operation_or = 52, type=<class 'str'>
# 	operation_not5 = 52, type=<class 'str'>
# 	operation_not6 = 52, type=<class 'str'>
# Переменные занимают: 424 байт

# Программа №3
# print("Введите две буквы:")
# letter1 = input("\tБуква 1 = ")
# letter2 = input("\tБуква 2 = ")
#
# pos1 = ord(letter1) - ord('a') + 1
# pos2 = ord(letter2) - ord('a') + 1
#
# print(f'Буква {letter1} находится в алфавите на позиции {pos1}')
# print(f'Буква {letter2} находится в алфавите на позиции {pos2}')
#
# distance = abs(pos1 - pos2) - 1
# if distance > 0:
#     print(f'Между буквами {letter1} и {letter2} находится {distance} букв')
# else:
#     print(f'Между буквами {letter1} и {letter2} нет других букв')
# **************************************************
# {'letter1': 'e', 'letter2': 'q', 'pos1': 5, 'pos2': 17, 'distance': 11}
# 	letter1 = 50, type=<class 'str'>
# 	letter2 = 50, type=<class 'str'>
# 	pos1 = 28, type=<class 'int'>
# 	pos2 = 28, type=<class 'int'>
# 	distance = 28, type=<class 'int'>
# Переменные занимают: 184 байт

# Окончание программы *************************************************

end_locals = locals().copy()

end_locals.pop('start_locals')
for key, _ in start_locals.items():
    end_locals.pop(key)

print('*' * 50)
print(end_locals)
print(f'Переменные занимают: {calc_total(end_locals)} байт')
