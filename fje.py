#!/usr/bin/env python

from abc import ABC, abstractmethod

class Node(ABC):
    @abstractmethod
    def display(self, prefix: str = '', is_last: bool = True) -> str:
        """
        显示节点
        :param prefix: 该节点的前缀字符串
        :param is_last: 表示是否是最后一个节点
        :return: 节点的字符串表示
        """
        pass

class TreeLeafNode(Node):
    def __init__(self, key, value, icon_family):
        self.icon_family = icon_family
        self.key = key  # 节点的键
        self.value = value # 节点的值

    def display(self, prefix: str = '', is_last: bool = True) -> str:
        node_prefix = '└─' if is_last else '├─'
        if self.value is None:
            return prefix + node_prefix + self.icon_family[1] + f"{self.key}"
        else:
            return prefix + node_prefix + self.icon_family[1] + f"{self.key}: {self.value}"

class TreeCompositeNode(Node):
    def __init__(self, key, icon_family):
        self.icon_family = icon_family
        self.key = key
        self.children = []
        self.level = 0

    def add(self, node: Node):
        node.level = self.level + 1
        self.children.append(node)

    def display(self, prefix: str = '', is_last: bool = True) -> str:
        node_prefix = '└─' if is_last else '├─'  # 根据是否是最后一个节点，选择前缀
        if self.level == 0:
            result = ''
        else:
            result = prefix + node_prefix + self.icon_family[0] + f"{self.key}\n"
        for i, child in enumerate(self.children):
            child_is_last = (i == len(self.children) - 1)   # 判断是否是最后一个节点
            # 如果是列表中最后一个子复合节点，其子节点前就不需要延续该子复合节点的竖线，反之需要延续
            child_prefix = '' if self.level==0 else ('   ' if is_last else '│  ')
            result += child.display(prefix + child_prefix, child_is_last) + '\n'
        return result.rstrip()


class NodeFactory(ABC):
    @abstractmethod
    def create_leaf_node(self, key, value, icon_family) -> Node:
        pass

    @abstractmethod
    def create_composite_node(self, key, icon_family) -> Node:
        pass


class TreeNodeFactory(NodeFactory):
    """
    树形结构
    """
    def create_leaf_node(self, key, value, icon_family) -> Node:
        """
        创建叶子节点
        :param key:
        :param value:
        :param icon_family:
        :return:
        """
        return TreeLeafNode(key, value, icon_family)

    def create_composite_node(self, key, icon_family) -> Node:
        return TreeCompositeNode(key, icon_family)



"""
----------------# 增加新的抽象工厂实现矩形结构 #----------------
"""
# 矩形结构的节点类实现
class RectangleLeafNode(Node):
    """
    矩形叶子节点
    """
    def __init__(self, key, value, icon_family, row_length=60):
        self.icon_family = icon_family
        self.key = key
        self.value = value
        self.row_length = row_length


    def display(self, prefix: str = '', is_last: bool = True) -> str:
        node_prefix = '└─' if is_last else '├─'
        if self.value is None:
            row = prefix + node_prefix + self.icon_family[1] + f"{self.key}"
            if len(row) < self.row_length:
                return row + '─' * (self.row_length - len(row) - 1) + '─┤'
        else:
            row = prefix + node_prefix + self.icon_family[1] + f"{self.key}: {self.value}"
            if len(row) < self.row_length:
                return row + '─' * (self.row_length - len(row) - 1) + '─┤'

class RectangleCompositeNode(Node):
    """
    矩形复合节点
    """
    def __init__(self, key, icon_family, row_length=60):
        self.icon_family = icon_family
        self.key = key
        self.children = []
        self.level = 0
        self.row_length = row_length

    def add(self, node: Node):
        node.level = self.level + 1
        self.children.append(node)

    def display(self, prefix: str = '', is_last: bool = True) -> str:
        node_prefix = '├─'  # 根据是否是最后一个节点，选择前缀
        if self.level == 0:
            result = ''
        else:
            row = prefix + node_prefix + self.icon_family[0] + f"{self.key}"
            result = row + '─' * (self.row_length - len(row) - 1) + '─┤' + '\n'
        for i, child in enumerate(self.children):
            child_is_last = (i == len(self.children) - 1)   # 判断是否是最后一个节点
            # 如果是列表中最后一个子复合节点，其子节点前就不需要延续该子复合节点的竖线，反之需要延续
            child_prefix = '' if self.level==0 else '│  '
            result += str(child.display(prefix + child_prefix, child_is_last)) + '\n'

        # 矩形边框处理
        if self.level == 0:
            result_list = list(result)
            result_list[0] = '┌'
            result_list[self.row_length] = '┐'
            result_list[-2] = '┘'
            result_list[-self.row_length-2] = '└'
            for i in range(-self.row_length-1, -1):
                if result_list[i] == '│' or result_list[i] == '├' or result_list[i] == '└':
                    result_list[i] = '┴'
                elif result_list[i] == ' ':
                    result_list[i] = '─'
                elif result_list[i] == self.icon_family[0] or result_list[i] == self.icon_family[1]:
                    break
            result = ''.join(result_list)
        return result.rstrip()

# 矩形结构的抽象工厂实现
class RectangleNodeFactory(NodeFactory):
    def create_leaf_node(self, key, value, icon_family) -> Node:
        return RectangleLeafNode(key, value, icon_family)

    def create_composite_node(self, key, icon_family) -> Node:
        return RectangleCompositeNode(key, icon_family)


class JSONBuilder:
    """
    JSON构建器
    """
    def __init__(self, factory: NodeFactory, icon_family = ['', '']):
        """
        :param factory: 传入的节点工厂
        :param icon_family: 传入的图标族
        """
        self.factory = factory
        self.icon_family = icon_family
    def build(self, json_data, key=None):
        """
        构建节点
        :param json_data: 传入的json数据
        :param key: 传入的键
        :return: 构建的节点
        """
        if isinstance(json_data, dict):
            node = self.factory.create_composite_node(key, self.icon_family)
            for k, v in json_data.items():
                child_node = self.build(v, k)
                node.add(child_node)
            return node
        elif isinstance(json_data, list):
            node = self.factory.create_composite_node(key, self.icon_family)
            for i, v in enumerate(json_data):
                child_node = self.build(v, f"{key}[{i}]")
                node.add(child_node)
            return node
        else:
            return self.factory.create_leaf_node(key, json_data, self.icon_family)


import json
import argparse

def parse_arguments():
    parser = argparse.ArgumentParser(description='Funny JSON Explorer')
    parser.add_argument('-f', '--file', required=True, help='JSON file to visualize')
    parser.add_argument('-s', '--style', required=False, default='tree', help='Display style')
    parser.add_argument('-i', '--icon', required=False, default='default', help='Icon family')
    return parser.parse_args()


def main():
    args = parse_arguments()

    with open(args.file, 'r') as f:
        json_data = json.load(f)

    icon_family = {
        'default': [' ', ' '],
        'tree': ['🌳', '🍂'],
        'star': ['⭐️', '✨'],
        'animal': ['🐿️', '🐾'],
        'tech': ['💻', '📱'],
        'food': ['🍎', '🍏'],
    }[args.icon]

    factory = {
        'tree': TreeNodeFactory(),
        'rectangle': RectangleNodeFactory()
    }[args.style]

    builder = JSONBuilder(factory, icon_family)
    root = builder.build(json_data)
    print(root.display())



if __name__ == '__main__':
    main()

