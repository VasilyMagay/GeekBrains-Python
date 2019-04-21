# Вводятся три разных числа. Найти, какое из них является средним (больше одного, но меньше другого).

print('Введите три разных числа:')
dig1 = float(input("\tЧисло 1 = "))
dig2 = float(input("\tЧисло 2 = "))
dig3 = float(input("\tЧисло 3 = "))

if dig2 > dig1 and dig3 > dig1:
    if dig2 > dig3:
        print(f'Среднее число: {dig3}')
    else:
        print(f'Среднее число: {dig2}')
elif dig1 > dig2 and dig3 > dig2:
    if dig1 > dig3:
        print(f'Среднее число: {dig3}')
    else:
        print(f'Среднее число: {dig1}')
elif dig1 > dig3 and dig2 > dig3:
    if dig1 > dig2:
        print(f'Среднее число: {dig2}')
    else:
        print(f'Среднее число: {dig1}')
else:
    print(f'Среднее число не определено')
