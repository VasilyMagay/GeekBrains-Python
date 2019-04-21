# Выполнить логические побитовые операции «И», «ИЛИ» и др. над числами 5 и 6.
# Выполнить над числом 5 побитовый сдвиг вправо и влево на два знака.

dig5 = 101
dig6 = 110

dig5_1 = dig5 // 100
dig5_2 = (dig5 % 100) // 10
dig5_3 = (dig5 % 100) % 10

dig6_1 = dig6 // 100
dig6_2 = (dig6 % 100) // 10
dig6_3 = (dig6 % 100) % 10

operation_and = f'{dig5_1 * dig6_1}{dig5_2 * dig6_2}{dig5_3 * dig6_3}'
operation_or = f'{1 if (dig5_1 + dig6_1) > 0 else 0}{1 if (dig5_2 + dig6_2) > 0 else 0}{1 if (dig5_3 + dig6_3) > 0 else 0}'
operation_not5 = f'{1 if dig5_1 == 0 else 0}{1 if dig5_2 == 0 else 0}{1 if dig5_3 == 0 else 0}'
operation_not6 = f'{1 if dig6_1 == 0 else 0}{1 if dig6_2 == 0 else 0}{1 if dig6_3 == 0 else 0}'

print(f'Операция "И" с числами {dig5} и {dig6}: {operation_and}')
print(f'Операция "ИЛИ" с числами {dig5} и {dig6}: {operation_or}')
print(f'Операция "НЕ" с числом {dig5}: {operation_not5}')
print(f'Операция "НЕ" с числом {dig6}: {operation_not6}')
print(f'Побитовый сдвиг числа {dig5} вправо на 2 знака: {dig5 // 100}')
print(f'Побитовый сдвиг числа {dig5} влево на 2 знака: {dig5 * 100}')
