# Посчитать, сколько раз встречается определенная цифра в введенной последовательности чисел.
# Количество вводимых чисел и цифра, которую необходимо посчитать, задаются вводом с клавиатуры.


def count_dig(num, dig):
    sum = 0
    for c in num:
        sum += (1 if c == dig else 0)
    return sum


n = int(input('Введите кол-во чисел в последовательности: '))
dig = input('Введите искомую цифру: ')

counter = 0
for i in range(n):
    counter += count_dig(input(f'Введите число №{i + 1}: '), dig)

print(f'Цифра {dig} встречается {counter} раз(а)')