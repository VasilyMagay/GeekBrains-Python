# Написать программу сложения и умножения двух шестнадцатеричных чисел. При этом каждое число представляется
# как массив, элементы которого — цифры числа. Например, пользователь ввёл A2 и C4F. Нужно сохранить их как
# [‘A’, ‘2’] и [‘C’, ‘4’, ‘F’] соответственно. Сумма чисел из примера: [‘C’, ‘F’, ‘1’], произведение -
# [‘7’, ‘C’, ‘9’, ‘F’, ‘E’].

from collections import deque

HEX_ALPHABET = list('0123456789ABCDEF')


def hex_sum(dig1, dig2):
    hex1 = deque(dig1)
    hex2 = deque(dig2)
    result = []
    addition = 0
    for i in range(max(len(hex1), len(hex2))):
        char1 = hex1.pop() if len(hex1) > 0 else '0'
        char2 = hex2.pop() if len(hex2) > 0 else '0'
        ind = HEX_ALPHABET.index(char1) + HEX_ALPHABET.index(char2) + addition
        addition, ind = divmod(ind, 16)
        result.append(HEX_ALPHABET[ind])
    if addition > 0:
        result.append(HEX_ALPHABET[addition])
    result.reverse()
    return result


def hex_multi(dig1, dig2):
    hex1 = deque(dig1)
    hex2 = deque(dig2)
    hex2.reverse()
    result = []
    for i in range(len(hex1)):
        line_result = list('0' * i)
        addition = 0
        char1 = hex1.pop()
        for j, char2 in enumerate(hex2):
            ind = HEX_ALPHABET.index(char1) * HEX_ALPHABET.index(char2) + addition
            addition, ind = divmod(ind, 16)
            line_result.append(HEX_ALPHABET[ind])
        if addition > 0:
            line_result.append(HEX_ALPHABET[addition])
            line_result.reverse()
        # print(line_result)
        result = hex_sum(result, line_result)
    return result


def to_dec(dig):
    return int(''.join(dig), 16)


dig1 = list(input('Первое шестнадцатеричное число: ').upper())
dig2 = list(input('Второе шестнадцатеричное число: ').upper())

s = hex_sum(dig1, dig2)
m = hex_multi(dig1, dig2)
print(f'{dig1} + {dig2} = {s} (проверка: {hex(to_dec(dig1) + to_dec(dig2))})')
print(f'{dig1} * {dig2} = {m} (проверка: {hex(to_dec(dig1) * to_dec(dig2))})')
