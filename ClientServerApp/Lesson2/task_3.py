# Задание на закрепление знаний по модулю yaml. Написать скрипт, автоматизирующий сохранение данных в файле
# YAML-формата. Для этого:
#
# Подготовить данные для записи в виде словаря, в котором первому ключу соответствует список, второму — целое число,
# третьему — вложенный словарь, где значение каждого ключа — это целое число с юникод-символом, отсутствующим в
# кодировке ASCII (например, €);
#
# Реализовать сохранение данных в файл формата YAML — например, в файл file.yaml. При этом обеспечить стилизацию файла
# с помощью параметра default_flow_style, а также установить возможность работы с юникодом: allow_unicode = True;
#
# Реализовать считывание данных из созданного файла и проверить, совпадают ли они с исходными.


import yaml

data = {
    'names': ['Peter', 'Ivan', 'John'],
    'groupID': 17,
    'funds': {r'€': 1000, r'£': 600}
}

filename = 'data/file.yml'

with open(filename, 'w', encoding='utf-8') as file:
    yaml.dump(data, file, default_flow_style=True, allow_unicode=True, sort_keys=False, Dumper=yaml.Dumper)

with open(filename, encoding='utf-8') as file:
    print(file.read())
