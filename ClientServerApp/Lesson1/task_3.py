# Определить, какие из слов «attribute», «класс», «функция», «type» невозможно записать в байтовом типе.


def convert2bytes(word):
    return bytes([ord(i) for i in word])


words_list = ['attribute', 'класс', 'функция', 'type']

word = words_list[3]
print(f'Слово: {word}\nБайт-строка: {convert2bytes(word)}')

# Слова "класс", "функция" невозможно записать в байтовом типе, т.к. каждая буква слова должна
# иметь код от 0 до 255. А при кодировке по умолчанию Unicode коды русских букв превышают данные ограничения.
