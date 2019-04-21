# Пользователь вводит две буквы. Определить, на каких местах алфавита они стоят, и сколько между ними находится букв.

print("Введите две буквы:")
letter1 = input("\tБуква 1 = ")
letter2 = input("\tБуква 2 = ")

pos1 = ord(letter1) - ord('a') + 1
pos2 = ord(letter2) - ord('a') + 1

print(f'Буква {letter1} находится в алфавите на позиции {pos1}')
print(f'Буква {letter2} находится в алфавите на позиции {pos2}')

distance = abs(pos1 - pos2) - 1
if distance > 0:
    print(f'Между буквами {letter1} и {letter2} находится {distance} букв')
else:
    print(f'Между буквами {letter1} и {letter2} нет других букв')
