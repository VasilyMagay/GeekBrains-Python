# Каждое из слов «class», «function», «method» записать в байтовом типе без преобразования в последовательность кодов
# (не используя методы encode и decode) и определить тип, содержимое и длину соответствующих переменных.

import sys


def print_var(var):
    print(f'\tЗначение={var}, Тип={type(var)}, Размер в памяти={sys.getsizeof(var)}')


words_list = ['class', 'function', 'method']

for w in words_list:
    print_var(w)
    print_var(bytes(w, 'utf-8'))
    print('')
