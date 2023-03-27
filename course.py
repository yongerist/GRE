class Course:
    id = None

    # id:,name:
    def __int__(self, id, name, begin_time, duration, week, offline):
        self.id = id
        self.name = name
        self.begin_time = begin_time
        self.duration = duration
        self.week = week
        self.offline = offline


class BPlusNode:
    def __init__(self, is_leaf=False):
        self.is_leaf = is_leaf
        self.keys = []
        self.values = []
        self.next = []

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
            return self.next.find_value(key)


class BPlusTree:
    def __init__(self):
        self.root = BPlusNode(is_leaf=True)

    #查询，从根节点开始查询
    def find(self, key):
        return self.root.find_value(key)

    # 必须是一个原树中没有的值
    def insert(self):

    def remove(self):
