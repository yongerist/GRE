import string


class Course:

    # id:,name:
    def __int__(self, id, name, begin_time, duration, week, offline):
        self.id: string = id
        self.name: string = name
        self.begin_time: int = begin_time
        self.duration: int = duration
        self.week: list < bool >= week
        self.offline: bool = offline


class BPlusNode:
    def __init__(self, is_leaf=False):
        self.is_leaf: bool = is_leaf
        self.keys = []
        self.values = []
        self.next = []  # 如果不是叶子节点next保存下一层节点，否则保存后续节点

    # 寻找key的索引，如果不是叶子节点，则返回下一层的节点，如果是叶子节点，则返回key的下标
    def find_index(self, key):
        left = 0
        right = len(self.keys) - 1
        while left <= right:
            mid = (right + left) // 2
            if self.keys[mid] == key:
                return mid
            elif self.keys[mid] > key:
                right = mid - 1
            else:
                left = mid + 1
        return left

    # 寻找key的值
    def find_value(self, key):
        index = self.find_index(key)
        """如果self.keys的长度不为0则说明，那么self是叶子节点，
           因为find_index中如果没有查询到对应的值，返回的是下一层的节点，这样在叶子节点中会返回错误的下标
           所以要检查查询到的值与key是否一样，如果一样返回对应的值，不一样则返回None"""
        if index < len(self.keys) and self.keys[index] == key:
            return self.values[index]
        elif self.is_leaf:
            return None
        else:
            return self.next[index].find_value(key)

    # 递归插入
    def insert(self, course):
        if not self.is_leaf:
            next_node = self.next[self.find_index(course.id)].insert(course)
            if next_node is not None:
                index = self.find_index(next_node.keys[0])
                self.keys.insert(index, next_node.keys[0])
                self.values.insert(index, next_node.values[0])
                self.next.insert(index, next_node)
        else:
            index = self.find_index(course.id)
            self.keys.insert(index, course.id)
            self.values.insert(index, course.id)
        if len(self.keys) > BPlusTree.max_keys:
            new_node = BPlusNode(self.is_leaf)
            mid_index = len(self.keys) // 2
            new_node.keys = self.keys[mid_index:]
            del self.keys[mid_index:]
            new_node.values = self.values[mid_index:]
            del self.values[mid_index:]
            if self.is_leaf:
                new_node.next = self.next
                self.next = new_node
            else:
                new_node.next = self.next[mid_index:]
                del self.next[mid_index:]
            return new_node
        return None


class BPlusTree:
    max_keys = 4
    min_keys = 2

    def __init__(self):
        self.root = BPlusNode(is_leaf=True)

    # 查询，从根节点开始查询
    def find(self, key):
        return self.root.find_value(key)

    # 插入
    def insert(self, course):
        new_node = self.root.insert(course)
        if new_node is not None:
            new_root=BPlusNode()
            new_root.keys.insert(self.root.keys[-1])
            new_root.next=[new_root,new_node]
            self.root=new_root

    # def remove(self):
