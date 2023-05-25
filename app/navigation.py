import heapq


class Graph:
    def __init__(self):
        self.nodes = {}  # 存储节点的字典，键为节点名称，值为节点属性
        self.edges = {}  # 存储边的字典，键为节点名称，值为该节点的相邻节点列表和对应的边权重

    def add_node(self, node, **kwargs):
        self.nodes[node] = kwargs  # 将节点及其属性添加到节点字典中

    def add_edge(self, src, dest, weight):
        if src not in self.edges:
            self.edges[src] = []  # 若起点不在边字典中，则将其添加为键，并对应一个空列表
        self.edges[src].append((dest, weight))  # 将目标节点和边权重添加到起点节点的相邻节点列表中

        if dest not in self.edges:
            self.edges[dest] = []  # 若终点不在边字典中，则将其添加为键，并对应一个空列表
        self.edges[dest].append((src, weight))  # 将起点节点和边权重添加到终点节点的相邻节点列表中

    def shortest_path(self, start, end):
        distances = {node: float('inf') for node in self.nodes}  # 存储起点到每个节点的最短距离，默认为正无穷
        distances[start] = 0  # 起点到起点的距离为0

        # 使用优先队列（最小堆）选择具有最小距离的节点
        pq = [(0, start)]
        while pq:
            curr_dist, curr_node = heapq.heappop(pq)  # 弹出具有最小距离的节点

            # 如果当前节点已经被访问过且距离更短，则跳过该节点
            if curr_dist > distances[curr_node]:
                continue

            # 检查邻居节点并更新距离
            for neighbor, edge_weight in self.edges[curr_node]:
                new_dist = curr_dist + edge_weight
                if new_dist < distances[neighbor]:  # 如果通过当前节点到达邻居节点的距离更短
                    distances[neighbor] = new_dist  # 更新邻居节点的最短距离
                    heapq.heappush(pq, (new_dist, neighbor))  # 将邻居节点和新距离加入优先队列

        # 重构最短路径
        path = [end]
        curr_node = end
        while curr_node != start:
            neighbors = self.edges[curr_node]
            prev_node = None
            min_dist = float('inf')
            for neighbor, _ in neighbors:
                if distances[neighbor] < min_dist:
                    min_dist = distances[neighbor]
                    prev_node = neighbor
            if prev_node is None:
                return None  # 不存在路径
            path.append(prev_node)
            curr_node = prev_node

        path.reverse()
        return path


G = Graph()

G.add_node("酒店", color='b')
G.add_node("学11公寓", color='b')
G.add_node('3', color='r')
G.add_node('4', color='r')
G.add_node('5', color='r')
G.add_node('经管楼', color='b')
G.add_node('7', color='r')
G.add_node('学六公寓', color='b')
G.add_node('9', color='r')
G.add_node('科研楼', color='b')
G.add_node('11', color='r')
G.add_node('教九', color='b')
G.add_node('学九和留学生公寓', color='b')
G.add_node('14', color='r')
G.add_node('学十', color='b')
G.add_node('16', color='r')
G.add_node('青年公寓', color='b')
G.add_node('18', color='r')
G.add_node('19', color='r')
G.add_node('新食堂', color='b')
G.add_node('21', color='r')
G.add_node('22', color='r')
G.add_node('物美和浴室', color='b')
G.add_node('24', color='r')
G.add_node("25", color='r')
G.add_node("学五公寓", color='b')
G.add_node('27', color='r')
G.add_node('学八公寓', color='b')
G.add_node('29', color='r')
G.add_node('麦当劳和学生发展中心', color='b')
G.add_node('学苑和老食堂', color='b')
G.add_node('学十三公寓', color='b')
G.add_node('学三公寓', color='b')
G.add_node('34', color='r')
G.add_node('学四公寓', color='b')
G.add_node('36', color='r')
G.add_node('37', color='r')
G.add_node('38', color='r')
G.add_node('档案馆', color='b')
G.add_node('40', color='r')
G.add_node('41', color='r')
G.add_node('42', color='r')
G.add_node('43', color='r')
G.add_node('44', color='r')
G.add_node('45', color='r')
G.add_node('46', color='r')
G.add_node('47', color='r')
G.add_node('48', color='r')
G.add_node("49", color='r')
G.add_node("学一公寓", color='b')
G.add_node('51', color='r')
G.add_node('学二公寓', color='b')
G.add_node('53', color='r')
G.add_node('图书馆', color='b')
G.add_node('办公楼', color='b')
G.add_node('篮球场', color='b')
G.add_node('57', color='r')
G.add_node('58', color='r')
G.add_node('59', color='r')
G.add_node('学二十九公寓', color='b')
G.add_node('邮局', color='b')
G.add_node('62', color='r')
G.add_node('教四', color='b')
G.add_node('64', color='r')
G.add_node('教一', color='b')
G.add_node('66', color='r')
G.add_node('科学会堂', color='b')
G.add_node('体育馆', color='b')
G.add_node('69', color='r')
G.add_node('体育场', color='b')
G.add_node('71', color='r')
G.add_node('72', color='r')
G.add_node('73', color='r')
G.add_node('74', color='r')
G.add_node('教三', color='b')
G.add_node('76', color='r')
G.add_node('主楼', color='b')
G.add_node('教二', color='b')
G.add_node('79', color='r')
G.add_node("80", color='r')
G.add_node('81', color='r')
G.add_node('82', color='r')
G.add_node('83', color='r')
G.add_node('创新楼', color='b')
G.add_node('85', color='r')
G.add_node('86', color='r')
G.add_node('校医院', color='b')
G.add_node('88', color='r')

G.add_edge('酒店', '学11公寓', weight=8)
G.add_edge('学11公寓', '88', weight=2)
G.add_edge('88', '3', weight=5)
G.add_edge('88', '教九', weight=3)
G.add_edge('3', '4', weight=12)
G.add_edge('4', '5', weight=9)
G.add_edge('5', '16', weight=1)
G.add_edge('5', '经管楼', weight=5)
G.add_edge('16', '学十', weight=7)
G.add_edge('16', '新食堂', weight=3)
G.add_edge('14', '教九', weight=2)
G.add_edge('14', '学十', weight=5)
G.add_edge('14', '学九和留学生公寓', weight=5)
G.add_edge('经管楼', '7', weight=7)
G.add_edge('7', '9', weight=12)
G.add_edge('9', '学六公寓', weight=5)
G.add_edge('9', '科研楼', weight=4)
G.add_edge('科研楼', '11', weight=16)
G.add_edge('11', '42', weight=15)
G.add_edge('42', '41', weight=6)
G.add_edge('41', '40', weight=14)
G.add_edge('41', '59', weight=12)
G.add_edge('59', '58', weight=2)
G.add_edge('59', '学二十九公寓', weight=3)
G.add_edge('58', '57', weight=12)
G.add_edge('57', '篮球场', weight=6)
G.add_edge('篮球场', '40', weight=6)
G.add_edge('40', '学苑和老食堂', weight=4)
G.add_edge('学苑和老食堂', '24', weight=4)
G.add_edge('24', '9', weight=7)
G.add_edge('24', '物美和浴室', weight=9)
G.add_edge('物美和浴室', '22', weight=9)
G.add_edge('22', '21', weight=6)
G.add_edge('21', '新食堂', weight=3)
G.add_edge('21', '19', weight=12)
G.add_edge('19', '14', weight=6)
G.add_edge('19', '18', weight=10)
G.add_edge('18', '青年公寓', weight=4)
G.add_edge('18', '25', weight=4)
G.add_edge('25', '学五公寓', weight=5)
G.add_edge('学五公寓', '27', weight=5)
G.add_edge('27', '19', weight=4)
G.add_edge('27', '学八公寓', weight=5)
G.add_edge('学八公寓', '29', weight=7)
G.add_edge('29', '21', weight=4)
G.add_edge('25', '学十三公寓', weight=4)
G.add_edge('学十三公寓', '学三公寓', weight=5)
G.add_edge('学三公寓', '34', weight=5)
G.add_edge('34', '27', weight=4)
G.add_edge('34', '学四公寓', weight=5)
G.add_edge('学四公寓', '36', weight=7)
G.add_edge('36', '29', weight=4)
G.add_edge('36', '37', weight=6)
G.add_edge('37', '麦当劳和学生发展中心', weight=4)
G.add_edge('麦当劳和学生发展中心', '22', weight=4)
G.add_edge('37', '38', weight=6)
G.add_edge('38', '档案馆', weight=6)
G.add_edge('档案馆', '40', weight=6)
G.add_edge('学十三公寓', '43', weight=4)
G.add_edge('43', '44', weight=10)
G.add_edge('44', '34', weight=4)
G.add_edge('44', '45', weight=12)
G.add_edge('45', '36', weight=4)
G.add_edge('43', '46', weight=4)
G.add_edge('46', '47', weight=10)
G.add_edge('47', '44', weight=4)
G.add_edge('47', '48', weight=12)
G.add_edge('48', '45', weight=4)
G.add_edge('46', '49', weight=4)
G.add_edge('49', '学一公寓', weight=5)
G.add_edge('学一公寓', '51', weight=5)
G.add_edge('51', '47', weight=4)
G.add_edge('51', '学二公寓', weight=6)
G.add_edge('学二公寓', '53', weight=6)
G.add_edge('53', '48', weight=4)
G.add_edge('53', '办公楼', weight=12)
G.add_edge('办公楼', '图书馆', weight=6)
G.add_edge('图书馆', '38', weight=6)
G.add_edge('办公楼', '57', weight=12)
G.add_edge('49', '邮局', weight=8)
G.add_edge('邮局', '62', weight=8)
G.add_edge('62', '教四', weight=11)
G.add_edge('教四', '64', weight=11)
G.add_edge('64', '53', weight=16)
G.add_edge('64', '教一', weight=12)
G.add_edge('教一', '66', weight=12)
G.add_edge('66', '57', weight=16)
G.add_edge('66', '科学会堂', weight=6)
G.add_edge('科学会堂', '69', weight=6)
G.add_edge('69', '体育馆', weight=8)
G.add_edge('体育馆', '58', weight=8)
G.add_edge('69', '体育场', weight=5)
G.add_edge('62', '71', weight=8)
G.add_edge('71', '72', weight=11)
G.add_edge('72', '教四', weight=8)
G.add_edge('72', '73', weight=11)
G.add_edge('73', '64', weight=8)
G.add_edge('71', '74', weight=8)
G.add_edge('74', '教三', weight=11)
G.add_edge('教三', '72', weight=8)
G.add_edge('教三', '76', weight=11)
G.add_edge('76', '73', weight=8)
G.add_edge('76', '教二', weight=12)
G.add_edge('教二', '主楼', weight=8)
G.add_edge('主楼', '教一', weight=8)
G.add_edge('教二', '79', weight=12)
G.add_edge('79', '66', weight=16)
G.add_edge('79', '80', weight=12)
G.add_edge('80', '69', weight=16)
G.add_edge('74', '81', weight=16)
G.add_edge('81', '82', weight=22)
G.add_edge('82', '76', weight=16)
G.add_edge('82', '83', weight=24)
G.add_edge('83', '79', weight=16)
G.add_edge('83', '创新楼', weight=6)
G.add_edge('创新楼', '85', weight=6)
G.add_edge('85', '80', weight=16)
G.add_edge('82', '86', weight=5)
G.add_edge('86', '校医院', weight=10)

# path = nx.shortest_path(G, "教三", "学五公寓", weight="weight")
path = G.shortest_path("主楼", "学五公寓")
print(path)
