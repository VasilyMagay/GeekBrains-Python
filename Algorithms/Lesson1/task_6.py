# Пользователь вводит номер буквы в алфавите. Определить, какая это буква.

num = int(input('Введите номер буквы в алфавите: '))

if 1 <= num <= 26:
    print(f'Под номером {num} буква "{chr(ord("a") + num -1)}"')
else:
    print('Буквы с таким номером нет')