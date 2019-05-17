# Пользователь вводит данные о количестве предприятий, их наименования и прибыль за 4 квартал (т.е. 4 числа)
# для каждого предприятия. Программа должна определить среднюю прибыль (за год для всех предприятий) и отдельно
# вывести наименования предприятий, чья прибыль выше среднего и ниже среднего.

from collections import namedtuple

Company = namedtuple('Company', ['name', 'quarter_sum', 'year_sum'])

num = int(input('Кол-во компаний: '))
companies = []
total = 0
for i in range(num):
    print('*' * 30)
    name = input(f'[Компания {i + 1}] наименование: ')
    q_sum = []
    for q_ind in range(4):
        q_sum.append(int(input(f'[Компания {i + 1}] прибыль {q_ind + 1}-й квартал: ')))
    current_company = Company(name, q_sum, sum(q_sum))
    companies.append(current_company)
    total += current_company.year_sum

print('*' * 30)
average = total / num
print(f'Средняя прибыль: {average}')
for comp in companies:
    if comp.year_sum != average:
        print(
            f'Компания "{comp.name}": прибыль ({comp.year_sum}) {"выше" if comp.year_sum > average else "ниже"} средней')
