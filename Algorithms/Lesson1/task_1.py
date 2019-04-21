# Найти сумму и произведение цифр трехзначного числа, которое вводит пользователь.

num = int(input('Введите целое трехзначное число: '))

hundreds = num // 100
decades = (num % 100) // 10
units = (num % 100) % 10

print(f'Сумма цифр: {hundreds + decades + units}')
print(f'Произведение цифр: {hundreds * decades * units}')
