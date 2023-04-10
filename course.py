import string


class Course:
    name: string
    id: string
    day: int
    begin_time: int
    duration: int
    week: list
    offline: bool
    student: list

    # id:,name:
    def __int__(self, name, day, begin_time, duration, week, offline, student):
        self.name: string = name
        self.id: string
        self.day = day
        self.begin_time: int = begin_time
        self.duration: int = duration
        self.week: list < bool >= week
        self.offline: bool = offline
        self.student = student

    def __init__(self, name, student):
        self.name: string = name
        self.id: string
        self.begin_time: int
        self.duration: int
        self.week: list = []
        self.offline: bool
        self.student = student

    def get_id(self):
        # print(type(self.name))
        unicode_points = [ord(ch) for ch in self.name]
        print(unicode_points)
        self.id = ''.join(str(point) for point in unicode_points)


class MyHash:
    my_hash_table: list = []
    empty: list = []

    def __init__(self):
        my_hash_table: list = []
        empty: list = []

    def insert(self, value):
        # 如果列表中有空值,则插入该节点，如果没有，则插入末尾
        if not self.empty:
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
        if self.find(old_course) is not None:
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
        if self.is_leaf and self.keys[index] == key:
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
                if len(self.keys) < BPlusTree.min_keys + 1:
                    return self.merge_leaves(parent, index)
                else:
                    return None
        # 如果不是叶子节点，且子节点返回了一个要删除的索引，则删除索引
        # print(f"delete_key:{delete_key}")
        if delete_key is not None:
            index = self.find_index(delete_key)
            self.keys.pop(index)
        if len(self.keys) < BPlusTree.min_keys:
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
        # print(f"{course.id}")
        # 如果根节点也要发生裂变则要创建新的根节点
        if new_node is not None:
            # print(f"new_node.keys:{new_node.keys}")
            new_root = BPlusNode()
            new_root.keys.insert(0, carry)
            new_root.next = [self.root, new_node]
            self.root = new_root
            # print(type(self.root.next))
        # print(f"{course.id}")

    def remove(self, name):
        # print(f"root:{self.root.keys}")
        self.root.remove(name, None)
        # 当头节点的索引被全部删除时，它唯一的孩子就是新的头节点
        if len(self.root.keys) == 0:
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
        all_data.extend(node.values)
        return all_data

    def prefix_search(self, name):
        return self.root.find_prefix_value(name)


class User:
    name: string
    id: int
    password: string
    academy: string
    is_student: bool

    def __init__(self, name, password, academy):
        self.name = name
        self.password = password
        self.academy = academy


class Teacher(User):
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


class Student(User):
    course: list  # 每个学生自己的课程
    student_class: int
    majors: string

    def __init__(self, name, password, academy, student_class, majors):
        super().__init__(name, password, academy)
        self.student_class = student_class
        self.majors = majors
        self.course = []
        self.is_student = True

    def sort_by_time(self):
        course_list = []
        dic = {}
        for cour in self.course:
            dic[cour.begintime + cour.day * 100] = cour
        for key in sorted(dic):
            course_list.append(dic[key])
        return course_list

    def sort_by_name(self):
        course_list = []
        dic = {}
        for cour in self.course:
            dic[cour.name] = cour
        for key in sorted(dic):
            course_list.append(dic[key])
        return course_list

    def sort_by_id(self):
        course_list = []
        dic = {}
        for cour in self.course:
            dic[cour.id] = cour
        for key in sorted(dic):
            course_list.append(dic[key])
        return course_list


class UserManagement:
    user_table: MyHash

    def __init__(self, user_table):
        self.user_table = user_table

    def sign_up_teacher(self, name, password, academy, course_tree, course_table):
        teacher = Teacher(name, password, academy, course_tree, course_table, self.user_table)
        self.user_table.insert(teacher)

    def sign_up_student(self, name, password, academy, student_class, majors):
        student = Student(name, password, academy, student_class, majors)
        self.user_table.insert(student)

    # 登陆成功返回用户，不成功返回None
    def login(self, user_id, password):
        user = self.user_table.find(user_id)
        if password == user.password:
            return user
        else:
            return None


# 先把课程的B+树、哈希，和学生的哈希读出来
course_tree = BPlusTree()
course_table = MyHash()
user_table = MyHash()
# 实例化用户管理对象
user_management = UserManagement(user_table)
# 注册
user_management.sign_up_teacher("teacher", "000", "1", course_tree, course_table)
user_management.sign_up_student("student1", "111", '1', "1", "0")
# 登录
teacher = user_management.login(0, "000")
student = user_management.login(1, "111")
# 面向用户操作
teacher.insert(Course("computer", [1]))
print(student.sort_by_name()[0].name)

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
