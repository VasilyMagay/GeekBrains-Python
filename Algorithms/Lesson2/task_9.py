# Среди натуральных чисел, которые были введены, найти наибольшее по сумме цифр.
# Вывести на экран это число и сумму его цифр.


def sum_dig(num):
    sum = 0
    for c in num:
        sum += int(c)
    return sum


max_sum = 0
max_number = 0
while True:
    cur_num = input('Введите натуральное число (0 - завершить ввод чисел): ')
    if int(cur_num) == 0:
        break
    cur_sum = sum_dig(cur_num)
    if cur_sum > max_sum:
        max_sum, max_number = cur_sum, cur_num

print(f'Наибольшее число по сумме цифр = {max_number}. Сумма его цифр = {max_sum}')
