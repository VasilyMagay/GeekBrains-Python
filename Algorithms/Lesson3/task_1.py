# В диапазоне натуральных чисел от 2 до 99 определить, сколько из них кратны любому из чисел в диапазоне от 2 до 9.

result = {i: [] for i in range(2, 10)}

i = 2
while i < 100:
    for ind, item in result.items():
        if i % ind == 0:
            item.append(i)
    i += 1

for ind, item in result.items():
    print(f'Числу {ind} кратно {len(item)} чисел. Числа: {item}')
