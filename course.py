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

    def __init__(self, id):
        self.id: string = id
        self.name: string = []
        self.begin_time: int = []
        self.duration: int = []
        self.week: list < bool >= []
        self.offline: bool = None


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
    def insert(self, key, value):
        # 先找到要插入的位置
        if self.is_leaf is False:
            print(f"key:{key}    index:{self.find_index(key)}")
            # 递归
            new_node = self.next[self.find_index(key)].insert(key, value)
            if new_node is not None:
                index = new_node.keys[0]
                # 如果下一层添加了新的节点，则把子节点添加到上一层的next中
                self.next.insert(index, new_node)
            else:
                index = None
        else:
            print(f"key:{key}    index:{self.find_index(key)}")
            index = self.find_index(key)
        # 插入
        if index is not None:
            self.keys.insert(index, key)
            self.values.insert(index, value)

            # 如果超过最大长度，则添加兄弟节点
            if len(self.keys) > BPlusTree.max_keys:
                sibling = BPlusNode(is_leaf=self.is_leaf)
                mid_index = len(self.keys) // 2
                sibling.keys = self.keys[mid_index:]
                sibling.values = self.values[mid_index:]
                self.keys = self.keys[:mid_index]
                self.values = self.values[:mid_index]
                # 如果是叶子节点则next保存兄弟节点
                if self.is_leaf:
                    sibling.next = self.next
                    self.next = [sibling]
                # 如果不是叶子节点则保存下一层的节点
                else:
                    sibling.next = self.next[mid_index:]
                    self.next = self.next[:mid_index]
                # 返回新节点的第一个key
                return sibling
            else:
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
    def insert(self, course: Course):
        new_node = self.root.insert(course.id, course)
        print(f"{course.id}")
        # 如果根节点也要发生裂变则要创建新的根节点
        if new_node is not None:
            new_root = BPlusNode()
            new_root.keys.insert(0, self.root.keys[-1])
            new_root.next = [new_root, new_node]
            self.root = new_root
            print(type(self.root.next))
        print(f"{course.id}")
    # def remove(self):


c = []
for i in range(0, 200):
    c.insert(i, Course(i))
tree = BPlusTree()
a = Course(1)
print(tree.find(key=2))
for i in range(0, 200):
    tree.insert(c[i])
    # print(i)
#print(tree.find(key=2))
