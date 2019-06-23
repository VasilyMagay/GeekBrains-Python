# Задание на закрепление знаний по модулю CSV. Написать скрипт, осуществляющий выборку определенных данных из файлов
# info_1.txt, info_2.txt, info_3.txt и формирующий новый «отчетный» файл в формате CSV.
# Для этого:
#
# Создать функцию get_data(), в которой в цикле осуществляется перебор файлов с данными, их открытие и считывание
# данных.
# В этой функции из считанных данных необходимо с помощью регулярных выражений извлечь значения параметров «Изготовитель
# системы», «Название ОС», «Код продукта», «Тип системы». Значения каждого параметра поместить в соответствующий список.
# Должно получиться четыре списка — например, os_prod_list, os_name_list, os_code_list, os_type_list. В этой же функции
# создать главный список для хранения данных отчета — например, main_data — и поместить в него названия столбцов отчета
# в виде списка: «Изготовитель системы», «Название ОС», «Код продукта», «Тип системы». Значения для этих столбцов также
# оформить в виде списка и поместить в файл main_data (также для каждого файла);
#
# Создать функцию write_to_csv(), в которую передавать ссылку на CSV-файл. В этой функции реализовать получение данных
# через вызов функции get_data(), а также сохранение подготовленных данных в соответствующий CSV-файл;
#
# Проверить работу программы через вызов функции write_to_csv().


import re
import csv

DATA_CATALOG = 'data/'
FILENAMES = ['info_1.txt', 'info_2.txt', 'info_3.txt']


def get_data():
    def __check_phrase__(my_str, my_phrase, my_list):
        result = re.search(my_phrase, my_str)
        if result is not None:
            my_list.append(my_str[result.end() + 1:].strip())

    main_data = ['Изготовитель системы', 'Название ОС', 'Код продукта', 'Тип системы']
    os_prod_list = list()
    os_name_list = list()
    os_code_list = list()
    os_type_list = list()

    for filename in FILENAMES:
        with open(DATA_CATALOG + filename, 'r') as file:
            for curr_str in file:
                __check_phrase__(curr_str, r'Изготовитель системы', os_prod_list)
                __check_phrase__(curr_str, r'Название ОС', os_name_list)
                __check_phrase__(curr_str, r'Код продукта', os_code_list)
                __check_phrase__(curr_str, r'Тип системы', os_type_list)

    return {
        'main_data': main_data,
        'os_prod_list': os_prod_list,
        'os_name_list': os_name_list,
        'os_code_list': os_code_list,
        'os_type_list': os_type_list,
    }


def write_to_csv(file):
    data = get_data()

    csv_w = csv.writer(file)
    csv_w.writerow(data['main_data'], )
    for i in range(len(FILENAMES)):
        row = list()
        row.append(data['os_prod_list'][i])
        row.append(data['os_name_list'][i])
        row.append(data['os_code_list'][i])
        row.append(data['os_type_list'][i])
        csv_w.writerow(row)


with open(DATA_CATALOG + 'main_data.csv', 'w', newline='') as file:
    write_to_csv(file)
