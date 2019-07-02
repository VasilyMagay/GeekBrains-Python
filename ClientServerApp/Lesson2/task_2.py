# Задание на закрепление знаний по модулю json. Есть файл orders в формате JSON с информацией о заказах. Написать
# скрипт, автоматизирующий его заполнение данными. Для этого:
#
# Создать функцию write_order_to_json(), в которую передается 5 параметров — товар (item), количество (quantity),
# цена (price), покупатель (buyer), дата (date). Функция должна предусматривать запись данных в виде словаря в файл
# orders.json. При записи данных указать величину отступа в 4 пробельных символа;
#
# Проверить работу программы через вызов функции write_order_to_json() с передачей в нее значений каждого параметра.

import json

FILENAME = 'data/orders.json'


def write_order_to_json(item, quantity, price, buyer, date, codepage='cp1251'):
    with open(FILENAME, encoding=codepage) as file:
        j = json.load(file)
    j['orders'].append({
        'item': item,
        'quantity': quantity,
        'price': price,
        'buyer': buyer,
        'date': date
    })
    with open(FILENAME, 'w', encoding=codepage) as file:
        json.dump(j, file, indent=4)


write_order_to_json('Ink pen', 1, 10000, 'Trump', '31.05.2019')
write_order_to_json('Ink pen red', 2, 5000, 'Trump', '01.06.2019')
