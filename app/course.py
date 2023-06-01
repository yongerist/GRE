import string


class Course:
    name: string
    id: string
    day: list
    begin_time: list
    end_time: list
    week: list
    offline: bool
    student: list

    # id:,name:
    def __init__(self, name, day, begin_time, end_time, week, offline, student, road):
        self.name: string = name
        self.day = [int(x) for x in day]
        begin_hour = int(begin_time[:2])
        begin_minute = int(begin_time[3:])
        self.begin_time: list = [begin_hour, begin_minute]
        end_hour = int(end_time[:2])
        end_minute = int(end_time[3:])
        self.end_time: list = [end_hour, end_minute]
        self.week: list = [int(x) for x in week]
        if offline == 1:
            self.offline: bool = True
        else:
            self.offline: bool = False
        self.student = [int(x) for x in student]
        self.test = None
        self.road = road


class Test:
    def __init__(self, name, day, begin_time, week, offline, student, road):
        self.name = name
        self.day = [int(x) for x in day]
        begin_hour = int(begin_time[:2])
        begin_minute = int(begin_time[3:])
        self.begin_time: list = [begin_hour, begin_minute]
        self.end_time: list = [begin_hour + 1]
        self.week: list = [int(x) for x in week]
        if student is not None:
            self.student = [int(x) for x in student]
        if offline == 1:
            self.offline: bool = True
        else:
            self.offline: bool = False
        self.road = road


class Activity:
    name: string
    day: list
    begin_time: list
    end_time: list
    week: list

    def __init__(self, name, day, begin_time, week, offline, student, road):
        self.name = name
        self.day = [int(x) for x in day]
        begin_hour = int(begin_time[:2])
        begin_minute = int(begin_time[3:])
        self.begin_time: list = [begin_hour, begin_minute]
        self.end_time: list = [begin_hour + 1]
        self.week: list = [int(x) for x in week]
        if student is not None:
            self.student = [int(x) for x in student]
        if offline == 1:
            self.offline: bool = True
        else:
            self.offline: bool = False
        self.road = road


# 简单的哈希表，使用平方取中法散列
"""class MyHash:
    my_hash_table: list = []
    fail_rate: int

    def __init__(self):
        self.my_hash_table: list = [None] * 100
        self.fail_rate = 0

    def insert(self, value):
        # 如果列表中有空值,则插入该节点，如果没有，则插入末尾
        if int(value.id) > 100:
            hash_id = (int(value.id) * int(value.id) // 10 ** len(value.id)) % len(self.my_hash_table)
        else:
            hash_id = int(value.id)
        if self.my_hash_table[hash_id] is None:
            self.my_hash_table[hash_id] = value
        else:
            # 如果存在冲突，则向后找到最近的一个None添加进去
            for x in range(hash_id, len(self.my_hash_table) + 1):
                self.fail_rate = self.fail_rate + 1
                if self.my_hash_table[x] is None:
                    self.my_hash_table[x] = value
        # 当失败率过高时，重构哈希表
        if self.fail_rate > len(self.my_hash_table) / 5:
            self.rehash()

    def find(self, value_id):
        if int(value_id) > 100:
            hash_id = (int(value_id) * int(value_id) // 10 ** len(value_id)) % len(self.my_hash_table)
        else:
            hash_id = int(value_id)
        if self.my_hash_table[hash_id].id == value_id:
            return self.my_hash_table[hash_id]
        else:
            for x in range(hash_id, len(self.my_hash_table) - 1):
                if self.my_hash_table[x].id == value_id:
                    return self.my_hash_table[x]

    def remove(self, value_id):
        if int(value_id) > 100:
            hash_id = (int(value_id) * int(value_id) // 10 ** len(value_id)) % len(self.my_hash_table)
        else:
            hash_id = int(value_id)
        if self.my_hash_table[hash_id].id == value_id:
            self.my_hash_table[hash_id] = None
        else:
            for x in range(hash_id, len(self.my_hash_table) - 1):
                if self.my_hash_table[x].id == value_id:
                    self.my_hash_table[x] = None

    # 先删再增
    def revise(self, old_course, new_course):
        if self.find(old_course) is not None:
            self.remove(old_course.id)
            self.insert(new_course)

    # 当哈希表容量不够或一次插入失败率过高时重构哈希表
    def rehash(self):
        temp = []
        # 将所有的值先暂存起来
        for value in self.my_hash_table:
            if value is not None:
                temp.append(value)
        self.my_hash_table = [None] * 10 * len(self.my_hash_table)
        for value in temp:
            self.insert(value)
        self.fail_rate = 0"""


class MyHash:
    my_hash_table: list = []
    empty: list = []

    def __init__(self):
        self.my_hash_table: list = []
        self.empty: list = []

    def insert(self, value):
        # 如果列表中有空值,则插入该节点，如果没有，则插入末尾
        if self.empty:
            hash_id = self.empty[-1]
        else:
            hash_id = len(self.my_hash_table)
        self.my_hash_table.insert(hash_id, value)
        value.id = hash_id

    def find(self, hash_id):
        if hash_id < len(self.my_hash_table):
            return self.my_hash_table[hash_id]
        else:
            return None

    def remove(self, hash_id):
        if hash_id < len(self.my_hash_table):
            self.my_hash_table[hash_id] = None
        else:
            print("hash 删除错误")

    def revise(self, old_course, new_course):
        if self.find(old_course.id) is not None:
            self.remove(old_course.id)
            self.insert(new_course)

    def empty(self):
        if len(self.my_hash_table) == 0:
            return True
        else:
            return False


class BPlusNode:
    is_leaf: bool  #
    keys: list  # 保存键
    values: list  # 保存值
    next: list  # 如果不是叶子节点next保存下一层节点，否则保存后续节点

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

    # 每个索引节点数据量较小使用顺序查找
    def find_next_index(self, key):
        for index in range(0, len(self.keys)):
            if key < self.keys[index]:
                # print(f"{key}<{self.keys[index]}")
                return index
        return len(self.keys)

    # 寻找key的值
    def find_value(self, key):
        index = self.find_index(key)
        """如果self.keys的长度不为0则说明，那么self是叶子节点，
           因为find_next_index中如果没有查询到对应的值，返回的是下一层的节点，这样在叶子节点中会返回错误的下标
           所以要检查查询到的值与key是否一样，如果一样返回对应的值，不一样则返回None"""
        if self.is_leaf and self.keys[index] == key:
            # print(f"key:{key},index:{index},keys:{self.keys}")
            # print(f"values[{index}].id:{self.values[index].id}")
            return self.values[index]
        elif self.is_leaf:
            return None
        else:
            next_index = self.find_next_index(key)
            # print(f"key:{key},next_index:{next_index},keys:{self.keys}")
            # print(f"next[{next_index}].keys:{self.next[next_index].keys}")
            return self.next[next_index].find_value(key)

    def find_prefix_value(self, key):
        index = self.find_index(key)
        # print(f"self.keys:{self.keys}")
        """如果self.keys的长度不为0则说明，那么self是叶子节点，
           因为find_next_index中如果没有查询到对应的值，返回的是下一层的节点，这样在叶子节点中会返回错误的下标
           所以要检查查询到的值与key是否一样，如果一样返回对应的值，不一样则返回None"""
        if self.is_leaf and len(self.keys) <= index:
            return None
        if self.is_leaf and key in self.keys[index]:
            value: list = []
            print("leaf")
            print(f"self.keys:{self.keys}")
            while index < len(self.keys):
                if key in self.keys[index]:
                    value.append(self.values[index])
                    index = index + 1
                else:
                    return value
            node = self
            while True:
                index = 0
                # 如果已经是最后一个节点就返回
                if not node.next:
                    return value
                # 否则继续深入
                node = node.next[0]
                while index < len(node.keys):
                    if key in node.keys[index]:
                        value.append(node.values[index])
                        index = index + 1
                    else:
                        return value
        elif self.is_leaf:
            print("leaf")
            print(f"self.keys:{self.keys}")
            return None
        else:

            next_index = self.find_next_index(key)
            return self.next[next_index].find_prefix_value(key)

    # 递归插入
    """如果不是叶子节点则继续深入，否则添加元素。如果添加了元素，则要检查是否超过了树的阶，如果超过了则要分裂产生兄弟节点并将兄弟节点返回
        这里设置了一个全局变量carry来保存要添加到父节点的索引。"""

    def insert(self, key, value):
        global carry
        # 先找到要插入的位置
        if self.is_leaf is False:
            # print(f"key:{key}    next_index:{self.find_next_index(key)}")
            # 如果不是叶子节点则递归深入
            new_node = self.next[self.find_next_index(key)].insert(key, value)
            # 如果有来自子节点的索引要添加到这一层
            if new_node is not None:
                key = carry
                # 要添加的位置
                index = self.find_index(key)
                self.keys.insert(index, key)
                # print(key)
                next_index = self.find_next_index(key)
                # print(f"new_node.keys[0]={carry}")
                # print(f"len:{len(self.next)},next_index:{next_index}")
                # 如果下一层添加了新的节点，则把子节点添加到上一层的next中
                self.next.insert(next_index, new_node)
            else:
                index = None
        else:
            # print(f"key:{key}    index:{self.find_index(key)}")
            index = self.find_index(key)
            self.keys.insert(index, key)
            self.values.insert(index, value)
        # 插入
        if index is not None:
            # 如果超过最大长度，则添加兄弟节点
            if len(self.keys) > BPlusTree.max_keys:
                sibling = BPlusNode(is_leaf=self.is_leaf)
                # print(f"len:{len(self.next)}")
                mid_index = len(self.keys) // 2
                # 保存要添加到父亲节点上的索引
                carry = self.keys[mid_index]
                # 如果是叶子节点则next保存兄弟节点
                if self.is_leaf:
                    sibling.next = self.next
                    self.next = [sibling]
                    sibling.keys = self.keys[mid_index:]
                    self.keys = self.keys[:mid_index]
                    sibling.values = self.values[mid_index:]
                    self.values = self.values[:mid_index]
                    # print(f"len:{len(self.next)}")
                # 如果不是叶子节点则保存下一层的节点
                else:
                    mid_next_index = len(self.next) // 2
                    sibling.keys = self.keys[mid_index + 1:]
                    self.keys = self.keys[:mid_index]
                    sibling.next = self.next[mid_next_index:]
                    self.next = self.next[:mid_next_index]
                    # print(f"mid={mid_index}len:{len(self.next)}")
                # 返回新节点
                return sibling
            else:
                return None

    """判断要向哪个节点合并或借元素"""

    def find_merge_index(self, parent):
        self_index = parent.next.index(self)
        # print(f"self_index:{self_index} len(parent.next):{len(parent.next)} parent.keys:{parent.keys}")
        # 如果本节点的索引是0，则合并右侧节点
        if self_index == 0:
            marge_index = self_index + 1
        # 如果本节点左侧节点没有元素可借，右侧有节点且有元素可借，则借右侧节点的元素
        elif len(parent.next) > self_index + 1 and len(parent.next[self_index - 1].keys) <= BPlusTree.min_keys < len(
                parent.next[self_index + 1].keys):
            marge_index = self_index + 1
        # 其他情况合并左侧节点或向左侧节点借元素
        else:
            # print("left node")
            marge_index = self_index - 1
        return marge_index

    """如果借了一个元素返回None，如果合并了一个节点返回父节点要删除的元素"""

    def merge_leaves(self, parent, index):
        if parent is None:
            return None
        # 本节点在父节点的索引
        self_index = parent.next.index(self)
        marge_index = self.find_merge_index(parent)
        marge_node = parent.next[marge_index]
        # print(f"marge_node.keys:{marge_node.keys}")
        # 如果有元素可借
        if len(marge_node.keys) > BPlusTree.min_keys:
            # print("borrow")
            # 如果要向右侧的节点借元素，因为借的是第一个元素，所以要将其在父节点上的索引改为其原来的第二个元素（新的第一个元素）
            if self_index < marge_index:
                self.keys.append(marge_node.keys[0])
                parent_change = parent.keys.index(self.keys[0])
                del self.keys[index]
                del self.values[index]
                marge_node.keys.pop(0)
                parent.keys[parent_change] = marge_node.keys[0]
                self.values.append(marge_node.values[0])
                marge_node.values.pop(0)
            # 如果要向左侧的节点借元素，因为改变了本节点的第一个元素，所以要将在父节点上的索引改为原来的左侧节点的末尾元素（新的第一个元素）
            else:
                # print(parent.keys)
                parent_change = parent.keys.index(self.keys[0])
                del self.keys[index]
                del self.values[index]
                self.keys.insert(0, marge_node.keys[-1])
                parent.keys[parent_change] = self.keys[0]
                marge_node.keys.pop()
                self.values.insert(0, marge_node.values[-1])
                marge_node.values.pop()
            # 因为已经修改了父节点上的索引，所以不需要再返回要向上修改的值
            return None
        # 如果没有元素可借，合并节点，并返回父节点中要删除的索引
        else:
            # 合并节点
            if self_index < marge_index:
                # print(f"{self_index} < {marge_index}")
                delete_key = marge_node.keys[0]
                self.keys.extend(marge_node.keys)
                self.values.extend(marge_node.values)
                self.next = marge_node.next
                parent.next.pop(marge_index)
                return delete_key
            else:
                delete_key = parent.keys[marge_index]
                # print(f"delete_key:{delete_key}")
                self.keys = marge_node.keys + self.keys
                self.values = marge_node.values + self.values
                parent.next.pop(marge_index)
                # print(self.keys)
                return delete_key

    def merge(self, parent):
        if parent is None:
            return None
        # 本节点在父节点的索引
        # print(f"parent.keys:{parent.keys},len(parent.next):{len(parent.next)}")
        self_index = parent.next.index(self)
        marge_index = self.find_merge_index(parent)
        marge_node = parent.next[marge_index]
        # 如果有元素可借
        # print(marge_node.keys)
        # print(f"len(marge_node.keys):{len(marge_node.keys)}")
        if len(marge_node.keys) > BPlusTree.min_keys:
            if self_index < marge_index:
                # print(self.keys)
                self.keys.append(parent.keys[self_index])
                parent.keys[self_index] = marge_node.keys[0]
                marge_node.keys.pop(0)
                self.next.append(marge_node.next[0])
                marge_node.next.pop(0)
            else:
                self.keys.insert(0, parent.keys[self_index - 1])
                parent.keys[self_index - 1] = marge_node.keys[-1]
                marge_node.keys.pop()
                self.next.insert(0, marge_node.next[-1])
                marge_node.next.pop()
            return None
        # 如果没有元素可借，从父节点取一个索引，再合并节点，返回父节点中要删除的索引
        else:
            # 如果要合并的节点在右侧，则新的索引要添加从父节点取的索引再加上要合并节点的索引
            if self_index < marge_index:
                self.keys = self.keys + [parent.keys[self_index]] + marge_node.keys
                # self.keys.extend(parent.keys[self_index])
                # self.keys.extend(marge_node.keys)
                self.next.extend(marge_node.next)
                parent.next.pop(marge_index)
                # print(self.keys)
                # print(parent.keys[self_index])
                return parent.keys[self_index]
            # 如果要合并的节点在左侧，则新的索引要在前面加上要合并节点的索引和从父节点取的索引
            else:
                # print("borrow")
                self.keys.insert(0, parent.keys[marge_index])
                self.keys = marge_node.keys + self.keys
                self.next = marge_node.next + self.next
                parent.next.pop(marge_index)
                return parent.keys[marge_index]

    def remove(self, key, parent):
        if self.is_leaf is False:
            # print(f"key:{key}    next_index:{self.find_next_index(key)}")
            # 如果不是叶子节点则递归深入
            # print(f"go:{self.keys}")
            delete_key = self.next[self.find_next_index(key)].remove(key, self)
        else:
            # 如果是叶子节点，则判断要删除的值是否存在
            # print(f"go:{self.keys}")
            index = self.find_index(key)
            # print(f"index:{index}")
            # 如果不存在返回None
            if index is None:
                return None
            else:
                # 如果存在删除keys和value

                # print(self.keys)
                if len(self.keys) < BPlusTree.min_keys + 1 and parent is not None:
                    return self.merge_leaves(parent, index)
                else:
                    del self.keys[index]
                    del self.values[index]
                    return None
        # 如果不是叶子节点，且子节点返回了一个要删除的索引，则删除索引
        # print(f"delete_key:{delete_key}")
        if delete_key is not None:
            index = self.find_index(delete_key)
            self.keys.pop(index)
        if len(self.keys) < BPlusTree.min_keys and parent is not None:
            return self.merge(parent)
        else:
            return None


class BPlusTree:
    max_keys = 4
    min_keys = 2

    def __init__(self):
        self.root = BPlusNode(is_leaf=True)

    # 查询，从根节点开始查询
    def find(self, name):
        return self.root.find_value(name)

    # 插入
    """如果根节点需要发生裂变，则产生一个新的头节点，它的两个next分别指向原根节点和新节点"""

    def insert(self, value):
        global carry
        new_node = self.root.insert(value.name, value)
        # print(f"{course1.id}")
        # 如果根节点也要发生裂变则要创建新的根节点
        if new_node is not None:
            # print(f"new_node.keys:{new_node.keys}")
            new_root = BPlusNode()
            new_root.keys.insert(0, carry)
            new_root.next = [self.root, new_node]
            self.root = new_root
            # print(type(self.root.next))
        # print(f"{course1.id}")

    def remove(self, name):
        # print(f"root:{self.root.keys}")
        self.root.remove(name, None)
        # 当头节点的索引被全部删除时，它唯一的孩子就是新的头节点
        if len(self.root.keys) == 0:
            if len(self.root.next) == 0:
                self.root = BPlusNode(is_leaf=True)
            else:
                self.root = self.root.next[0]

    """修改成功返回Ture，失败返回False"""

    def revise(self, old_value, new_value):
        if self.find(old_value.name) is not None:
            # 先插入新值，再删除旧值
            self.insert(new_value)
            self.remove(old_value.name)
            return True
        else:
            return False

    """获取全部数据"""

    def get_all_data(self):
        # print("get")
        node = self.root
        # 从根节点下探到最左侧的叶子节点
        while node.is_leaf is False:
            node = node.next[0]
        # print(node.keys)
        all_data = node.values
        # 依次获取全部节点的数据
        while len(node.next) != 0:
            # print(node.next[0].keys)
            all_data.extend(node.next[0].values)
            node = node.next[0]
        return all_data

    def prefix_search(self, name):
        return self.root.find_prefix_value(name)


class Usr:
    name: string
    email: string
    id: string

    def __init__(self, username, email, userNumber):
        self.name = username
        self.email = email
        self.id = userNumber


class Teacher(Usr):
    user_table: MyHash
    course_tree: BPlusTree
    course_table: MyHash

    def __init__(self, name, password, academy, course_tree, course_table, user_table):
        super().__init__(name, password, academy)
        self.course_table = course_table
        self.course_tree = course_tree
        self.is_student = False
        self.user_table = user_table

    def insert(self, course):
        self.course_tree.insert(course)
        self.course_table.insert(course)
        for st in course.student:
            self.user_table.find(st).course.append(course)

    def remove(self, course):
        self.course_tree.remove(course.name)
        self.course_table.remove(course.id)

    def revise(self, old_course, new_course):
        self.course_tree.revise(old_course, new_course)
        self.course_table.revise(old_course, new_course)

    # 通过名称查找
    def find_by_name(self, name):
        return self.course_tree.find(name)

    # 通过名称的前缀查找
    def prefix_search(self, name):
        return self.course_tree.prefix_search(name)

    # 通过id查找
    def find_by_id(self, hash_id):
        return self.course_table.find(hash_id)


class Student(Usr):
    course: list  # 每个学生自己的课程,只存课程的id而不是课程的类
    student_class: int
    majors: string
    personal_activities: BPlusTree
    clock: dict

    def __init__(self, username, email, userNumber):
        super().__init__(username, email, userNumber)
        self.course = []
        day = [None] * 25
        week = []
        for _ in range(8):
            week.append(day.copy())
        time = []
        for _ in range(17):
            time.append([w.copy() for w in week])
            self.time = time
        self.personal_activities = BPlusTree()
        self.group_activities = []
        self.thing = BPlusTree()
        self.clock = {}

    def find_all_by_time(self, week, day, begin_time, end_time):
        personal_activities_list = []
        group_activities_list = []
        thing_list = []
        test_list = []
        course_list = []
        for i in range(begin_time, end_time + 1):
            if self.time[week][day][i] is not None:
                if "temp_thing" in self.time[week][day][i]:
                    temp = self.time[week][day][i].split("/")
                    for z in temp:
                        temp1 = z.split(" ")
                        thing_list.append(temp1[1])
                elif "test" in self.time[week][day][i]:
                    temp = self.time[week][day][i].split(" ")
                    test_list.append(temp[1])
                elif self.time[week][day][i][0] == 'p':
                    temp = self.time[week][day][i].split(" ")
                    personal_activities_list.append(temp[1])
                elif self.time[week][day][i][0] == 'c':
                    temp = self.time[week][day][i].split(" ")
                    if len(course_list) != 0:
                        if course_list[-1] != temp[1]:
                            course_list.append(temp[1])
                    else:
                        course_list.append(temp[1])
                else:
                    temp = self.time[week][day][i].split(" ")
                    group_activities_list.append(temp[1])
        return [course_list, test_list, group_activities_list, personal_activities_list, thing_list]

    def find_course_by_time(self, week, day, begin_time, end_time, tree):
        course_list = []
        for i in range(begin_time, end_time + 1):
            if self.time[week][day][i] is not None:
                if self.time[week][day][i][0] == 'c':
                    temp = self.time[week][day][i].split(" ")
                    if len(course_list) != 0:
                        if course_list[-1].name != temp[1]:
                            course_list.append(tree.find(temp[1]))
                    else:
                        course_list.append(tree.find(temp[1]))


    def find_group_activity_by_time(self, week, day, begin_time, end_time, tree):
        group_activity = []
        for i in range(begin_time, end_time + 1):
            if self.time[week][day][i] is not None:
                if self.time[week][day][i][0] == 'g':
                    temp = self.time[week][day][i].split(" ")
                    if len(group_activity) != 0:
                        if group_activity[-1].name != temp[1]:
                            group_activity.append(tree.find(temp[1]))
                    else:
                        group_activity.append(tree.find(temp[1]))

    def find_personal_activity_by_time(self, week, day, begin_time, end_time):
        course_list = []
        for i in range(begin_time, end_time + 1):
            if self.time[week][day][i] is not None:
                if self.time[week][day][i][0] == 'c':
                    temp = self.time[week][day][i].split(" ")
                    if len(course_list) != 0:
                        if course_list[-1].name != temp[1]:
                            course_list.append(self.personal_activities.find(temp[1]))
                    else:
                        course_list.append(self.personal_activities.find(temp[1]))

    def find_thing_by_time(self, week, day, begin_time, end_time):
        thing_list = []
        for i in range(begin_time, end_time + 1):
            if self.time[week][day][i] is not None:
                if "temp_thing" in self.time[week][day][i]:
                    temp = self.time[week][day][i].split(" ")
                    if len(thing_list) != 0:
                        if thing_list[-1].name != temp[1]:
                            thing_list.append(self.thing.find(temp[1]))
                    else:
                        thing_list.append(self.thing.find(temp[1]))

    def find_clock(self, week, day, hour):
        return self.clock.get(f"{week}+{day}+{hour}", " ")

    def add_clock(self, week, day, hour, name):
        for w in week:
            for d in day:
                for h in hour:
                    if not self.clock.get(f"{week}+{day}+{hour}", " "):
                        str = self.clock.get(f"{week}+{day}+{hour}", " ")
                        str += name + " "
                        self.clock[f"{w}+{d}+{h}"] = name + " "
                    else:
                        self.clock[f"{w}+{d}+{h}"] = name + " "

    def get_all_course(self, course_hash):
        course_list = []
        for x in self.course:
            course_list.append(course_hash.find(x))
        return course_list

    def get_all_group_activities(self, group_activities_tree):
        course_list = []
        for x in self.course:
            course_list.append(group_activities_tree.find(x))
        return course_list

    def time_conflicts(self, activity):
        for week in activity.week:
            for x in activity.day:
                for i in range(activity.begin_time[0], activity.end_time[0]):
                    if self.time[week][x][i] is not None:
                        print(f"{week},{x},{i}{self.time[week][x][i]}")
                        print("False")
                        return False
        print("true")
        return True

    def add_personal_activities(self, activity):
        self.personal_activities.insert(activity)
        for week in activity.week:
            for x in activity.day:
                for i in range(activity.begin_time[0], activity.end_time[0]):
                    self.time[week][x][i] = "personal_activity " + activity.name

    def del_personal_activities(self, activity):
        self.personal_activities.remove(activity.name)
        for week in activity.week:
            for x in activity.day:
                for i in range(activity.begin_time[0], activity.end_time[0]):
                    self.time[week][x][i] = None

    def auto_schedule(self, activity):
        for week in range(1, 17):
            for day in range(1, 8):
                for i in range(6, 23):
                    if self.time[week][day][i] is None:
                        activity.week = [week]
                        activity.day = [day]
                        activity.begin_time = [i]
                        activity.end_time = [i + 1]
                        return activity

    # 临时事务的时间检验
    def temp_time_conflicts(self, activity):
        for week in activity.week:
            for x in activity.day:
                for i in range(activity.begin_time[0], activity.end_time[0]):
                    if self.time[week][x][i] is not None:
                        if self.time[week][x][i][0] != 't':
                            return False
        print("true")
        return True

    def add_temp_thing(self, activity):
        self.thing.insert(activity)
        for week in activity.week:
            for x in activity.day:
                for i in range(activity.begin_time[0], activity.end_time[0]):
                    if self.time[week][x][i] is not None:
                        self.time[week][x][i] = self.time[week][x][i] + "/temp_thing " + activity.name
                    else:
                        self.time[week][x][i] = "temp_thing " + activity.name

    def find_temp_thing(self, activity_name):
        return self.personal_activities.find(activity_name)

    def del_temp_thing(self, activity):
        self.thing.remove(activity.name)
        for week in activity.week:
            for x in activity.day:
                for i in range(activity.begin_time[0], activity.end_time[0]):
                    if self.time[week][x][i] == "temp_thing " + activity.name:
                        self.time[week][x][i] = None
                    else:
                        temp = "/temp_thing " + activity.name
                        self.time[week][x][i] = self.time[week][x][i].replace(temp, "")
                        temp = "temp_thing " + activity.name + "/"
                        self.time[week][x][i] = self.time[week][x][i].replace(temp, "")

    def find_course(self, name, tree):
        course_list = tree.prefix_search(name)
        pop_list = []
        if course_list is None:
            return []
        for i in range(0, len(course_list)):
            if self.name in course_list[i].student:
                pop_list.append(i)
        for i in pop_list:
            course_list.pop(i)
        return course_list


class UserManagement:
    user_table: MyHash

    def __init__(self, user_table):
        self.user_table = user_table

    def user_init(self, username, email, userNumber):
        user = Student(username, email, userNumber)
        self.user_table.insert(user)
        print(user.id)

    # 登陆成功返回用户，不成功返回None
    def login(self, user_id):
        user = self.user_table.find(user_id)
        return user

    def all_student(self):
        return self.user_table.my_hash_table

    # 如果没有时间冲突则添加活动并返回true，有时间冲突返回false
    def add_student_activities(self, activity):
        for st in activity.student:
            self.user_table.find(st).group_activities.append(activity.name)
            for week in activity.week:
                for x in activity.day:
                    for i in range(activity.begin_time[0], activity.end_time[0]):
                        print("add")
                        print(f"{week},{x},{i}")
                        self.user_table.find(st).time[week][x][i] = "group_activity " + activity.name

    def del_student_activities(self, activity):
        for st in activity.student:
            self.user_table.find(st).group_activities.remove(activity.name)
            for week in activity.week:
                for x in activity.day:
                    for i in range(activity.begin_time[0], activity.end_time[0]):
                        self.user_table.find(st).time[week][x][i] = None

    def possible_time(self, activity):
        p_time = []
        for st in activity.student:
            for week in activity.week:
                for x in activity.day:
                    for i in range(6, 22):
                        # print(f"{week},{x},{i} {self.user_table.find(st).time[week][x][i]}")
                        if len(p_time) >= 3:
                            return p_time
                        if self.user_table.find(st).time[week][x][i] is None:
                            p_time.append(str(week) + "周" + str(x) + "日" + str(i) + "时")
        if not p_time:
            dic = {}
            for st in activity.student:
                for week in activity.week:
                    for x in activity.day:
                        for i in range(6, 22):
                            if self.user_table.find(st).time[week][x][i] is None:
                                dic[str(week) + "周" + str(x) + "日" + str(i) + "时"] = dic.get(
                                    str(week) + "周" + str(x) + "日" + str(i) + "时", 0) + 1

    def revise_student_activity(self, old_activity, new_activity):
        self.del_student_activities(old_activity)
        self.add_student_activities(new_activity)

    def auto_schedule(self, activity):
        for week in range(1, 17):
            for day in range(1, 8):
                for i in range(6, 23):
                    for st in activity.student:
                        if st == activity.student[-1] and self.user_table.find(st).time[week][day][i] is None:
                            activity.week = [week]
                            activity.day = [day]
                            activity.begin_time = [i]
                            activity.end_time = [i + 1]
                            return activity
                        if self.user_table.find(st).time[week][day][i] is not None:
                            break

    def add_student_test(self, test):
        for st in test.student:
            for week in test.week:
                for x in test.day:
                    for i in range(test.begin_time[0], test.end_time[0]):
                        print("add")
                        print(f"{week},{x},{i}")
                        self.user_table.find(st).time[week][x][i] = "test " + test.name

    def del_student_test(self, test):
        for st in test.student:
            for week in test.week:
                for x in test.day:
                    for i in range(test.begin_time[0], test.end_time[0]):
                        self.user_table.find(st).time[week][x][i] = None

    def revise_student_test(self, old_test, new_test):
        self.del_student_test(old_test)
        self.add_student_test(new_test)

    def add_student_course(self, course):
        for st in course.student:
            self.user_table.find(st).course.append(course.id)
            for week in course.week:
                for x in course.day:
                    for i in range(course.begin_time[0], course.end_time[0]):
                        print("add")
                        print(f"{week},{x},{i}")
                        self.user_table.find(st).time[week][x][i] = "course " + course.name
                        print("add")

    def time_conflicts(self, course):
        for st in course.student:
            for week in course.week:
                for x in course.day:
                    for i in range(course.begin_time[0], course.end_time[0]):
                        print(f"{week},{x},{i} {self.user_table.find(st).time[week][x][i]}")
                        if self.user_table.find(st).time[week][x][i] is not None:
                            # print(f"{week},{x},{i} {self.user_table.find(st).time[week][x][i]}")
                            print("False")
                            return False
        print("true")
        return True

    def del_student_course(self, course):
        print(course)
        for st in course.student:
            self.user_table.find(st).course.remove(course.id)
            for week in course.week:
                for x in course.day:
                    for i in range(course.begin_time[0], course.end_time[0]):
                        print("del")
                        print(f"{week},{x},{i}")
                        self.user_table.find(st).time[week][x][i] = None

    def revise_time_conflicts(self, old_course, new_course):
        if isinstance(old_course, Course):
            header = "course "
        elif isinstance(old_course, Activity):
            header = "group_activity "
        elif isinstance(old_course, Test):
            header = "test "
        for st in old_course.student:
            for week in old_course.week:
                for x in old_course.day:
                    for i in range(old_course.begin_time[0], old_course.end_time[0]):
                        self.user_table.find(st).time[week][x][i] = None
        if self.time_conflicts(new_course):
            for st in old_course.student:
                for week in old_course.week:
                    for x in old_course.day:
                        for i in range(old_course.begin_time[0], old_course.end_time[0]):
                            self.user_table.find(st).time[week][x][i] = header + old_course.name
            return True
        else:
            for st in old_course.student:
                for week in old_course.week:
                    for x in old_course.day:
                        for i in range(old_course.begin_time[0], old_course.end_time[0]):
                            self.user_table.find(st).time[week][x][i] = header + old_course.name
            return False

    def revise_student_course(self, old_course, new_course):
        self.del_student_course(old_course)
        self.add_student_course(new_course)


def quicksort_by_time(mylist, start, end):  # start,end 是指指针
    i, j = start, end
    if start < end:
        base = mylist[i]  # 设置基准数为i,即为start
        while i < j:
            while (i < j) and mylist[j].begin_time[0] + mylist[j].day[0] * 100 + mylist[j].week[0] * 1000 >= \
                    base.begin_time[0] + base.day[0] * 100 + base.week[0] * 1000:  # 找到比基准数小的数字
                j -= 1  # 将炮兵j向左移动
            mylist[i] = mylist[j]  # 将找到的j复制给i
            # 同样的方法执行前半区域
            while (i < j) and mylist[j].begin_time[0] + mylist[j].day[0] * 100 + mylist[j].week[0] * 1000 <= \
                    base.begin_time[0] + base.day[0] * 100 + base.week[0] * 1000:
                i += 1
            mylist[j] = mylist[i]
        mylist[i] = base  # i=j,即将这个数设置为base

        quicksort_by_time(mylist, start, i - 1)
        quicksort_by_time(mylist, j + 1, end)
    return mylist


def quicksort_by_name(mylist, start, end):  # start,end 是指指针
    i, j = start, end
    if start < end:
        base = mylist[i]  # 设置基准数为i,即为start
        while i < j:
            while (i < j) and mylist[j].name >= base.name:  # 找到比基准数小的数字
                j -= 1  # 将炮兵j向左移动
            mylist[i] = mylist[j]  # 将找到的j复制给i
            # 同样的方法执行前半区域
            while (i < j) and mylist[i].name <= base.name:
                i += 1
            mylist[j] = mylist[i]
        mylist[i] = base  # i=j,即将这个数设置为base

        quicksort_by_name(mylist, start, i - 1)
        quicksort_by_name(mylist, j + 1, end)
    return mylist


def quicksort_by_id(mylist, start, end):  # start,end 是指指针
    i, j = start, end
    if start < end:
        base = mylist[i]  # 设置基准数为i,即为start
        while i < j:
            while (i < j) and mylist[j].id >= base.id:  # 找到比基准数小的数字
                j -= 1  # 将炮兵j向左移动
            mylist[i] = mylist[j]  # 将找到的j复制给i
            # 同样的方法执行前半区域
            while (i < j) and mylist[i].id <= base.id:
                i += 1
            mylist[j] = mylist[i]
        mylist[i] = base  # i=j,即将这个数设置为base

        quicksort_by_id(mylist, start, i - 1)
        quicksort_by_id(mylist, j + 1, end)
    return mylist


"""def sort_by_time(unsorted_list):
    sorted_list = []
    dic = {}
    for x in unsorted_list:
        dic[unsorted_list[x].begintime + unsorted_list[x].day * 100] = unsorted_list[x]
    for key in sorted(dic):
        sorted_list.append(dic[key])
    return sorted_list


# 可以排用哈希存储的课程也可以排用b+树存储的课外活动
def sort_by_name(unsorted_list):
    sorted_list = []
    dic = {}
    for x in unsorted_list:
        dic[unsorted_list[x].name] = unsorted_list[x]
    for key in sorted(dic):
        sorted_list.append(dic[key])
    return sorted_list


def sort_by_id(unsorted_list):
    sorted_list = []
    dic = {}
    for x in unsorted_list:
        dic[unsorted_list[x].id] = unsorted_list[x]
    for key in sorted(dic):
        sorted_list.append(dic[key])
    return sorted_list"""

# # 先把课程的B+树、哈希，和学生的哈希读出来
# course_tree = BPlusTree()
# course_table = MyHash()
# user_table = MyHash()
# # 实例化用户管理对象
# user_management = UserManagement(user_table)
# # 注册
# # user_management.sign_up_teacher("teacher", "000", "1", course_tree, course_table)
# # user_management.sign_up_student("student1", "111", '1', "1", "0")
# # 登录
# teacher = user_management.login(0, "000")
# student = user_management.login(1, "111")
# # 面向用户操作
# teacher.insert(Course("computer", [1]))
# print(student.sort_by_name()[0].name)

"""c = []
for i in range(0, 2000):
    c.insert(i, Course("str:" + str(i)))
course_tree = BPlusTree()
my_hash = MyHash()
# a = Course(1)
# print(tree.find(key=200))

for i in range(0, 500):
    course_tree.insert(c[i])
    # my_hash.insert(c[i])
    # print(i)
for i in range(500, 1001):
    course_tree.insert(c[i])
    # my_hash.insert(c[i])
for i in range(1500, 1000, -1):
    course_tree.insert(c[i])
    # my_hash.insert(c[i])
for i in range(0, 100):
    # print(f"remove{i}")
    course_tree.remove("str:" + str(i))
for i in range(1000, 1400):
    # print(f"remove{i}")
    course_tree.remove("str:" + str(i))
course_tree.insert(c[1100])
course_tree.revise(c[1100], c[1101])
for i in range(100, 500):
    print(course_tree.find(name="str:" + str(i)).name)
print(course_tree.find(name="str:" + str(1)).name)
for i in course_tree.prefix_search(name="str:" + str(10)):
    print(i.name)  # 打印查找结果，如果查找成功则打印id,未作非法检验
course_tree.get_all_data()"""
