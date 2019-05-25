# Алгоритм кодирования Хаффмана

from collections import Counter


class MyNode:
    def __init__(self, value, num, left=None, right=None):
        self.value = value
        self.num = num
        self.left = left
        self.right = right


def haffman_coding(my_str):
    assert len(my_str) > 0, 'Задана пустая строка'

    def sorted_add(node_list, node):
        if len(node_list) == 0:
            node_list.append(node)
        else:
            is_added = False
            for i in range(len(node_list)):
                if node.num <= node_list[i].num:
                    node_list.insert(i, node)
                    is_added = True
                    break
            if not is_added:
                node_list.append(node)

    def find_values_in_tree(node, my_dict, path=''):
        if node.left is None and node.right is None:
            my_dict[node.value] = path
        if node.left is not None:
            find_values_in_tree(node.left, my_dict, path=f'{path}0')
        if node.right is not None:
            find_values_in_tree(node.right, my_dict, path=f'{path}1')

    # Получаем частотный словать
    res = Counter(my_str)
    print(f'Частота букв: {res}')

    node_list = []  # сортированный список элементов с листьями будующего дерева
    while len(res) > 0:
        item_tuple = res.popitem()
        sorted_add(node_list, MyNode(item_tuple[0], item_tuple[1]))

    haffman_dict = {i.value: '' for i in node_list}  # кодовый словарь "Хаффмана"

    if len(node_list) == 1:
        haffman_dict[node_list[0].value] = '0'
    else:
        # Формируем "дерево Хаффмана"
        while len(node_list) > 1:
            # print([(i.value, i.num) for i in node_list])
            # Вытаскиваем из списка два узла слева и подчиняем их новому узлу
            first_node = node_list[0]
            second_node = node_list[1]
            node_list = node_list[2:]
            merge_node = MyNode('', first_node.num + second_node.num, first_node, second_node)
            # Помещаем новый узел согласно отсортированным элементам в списке
            sorted_add(node_list, merge_node)
        # print([(i.value, i.num) for i in node_list])

        find_values_in_tree(node_list[0], haffman_dict)

    print(f'Кодовый словарь: {haffman_dict}')

    # Формируем закодированную строку
    result = ''
    for i in my_str:
        result += f'{haffman_dict[i]} '

    return result


my_str = input('Введите строку: ')
print(f'Закодированная строка: {haffman_coding(my_str)}')
