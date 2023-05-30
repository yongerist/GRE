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

G.add_node("酒店", color='b', x=1)
G.add_node("学11公寓", color='b')
G.add_node('美团外卖柜', color='r')
G.add_node('北门', color='r')
G.add_node('学十东路口', color='r')
G.add_node('经管楼', color='b')
G.add_node('综合服务楼北路口', color='r')
G.add_node('学六公寓', color='b')
G.add_node('京东快递站南路口', color='r')
G.add_node('科研楼', color='b')
G.add_node('东北门', color='r')
G.add_node('教九', color='b')
G.add_node('学九和留学生公寓', color='b')
G.add_node('综合食堂西北路口', color='r')
G.add_node('学十', color='b')
G.add_node('综合食堂东北路口', color='r')
G.add_node('青年公寓', color='b')
G.add_node('学五西北路口', color='r')
G.add_node('综合食堂西南路口', color='r')
G.add_node('新食堂', color='b')
G.add_node('综合食堂东南路口', color='r')
G.add_node('学生活动中心南侧', color='r')
G.add_node('物美和浴室', color='b')
G.add_node('科研楼西路口', color='r')
G.add_node("学五西南路口", color='r')
G.add_node("学五公寓", color='b')
G.add_node('学五东南路口', color='r')
G.add_node('学八公寓', color='b')
G.add_node('大电视北路口', color='r')
G.add_node('麦当劳和学生发展中心', color='b')
G.add_node('学苑和老食堂', color='b')
G.add_node('学十三公寓', color='b')
G.add_node('学三公寓', color='b')
G.add_node('学三东北路口', color='r')
G.add_node('学四公寓', color='b')
G.add_node('大电视南路口', color='r')
G.add_node('小松林北侧', color='r')
G.add_node('学生发展中心南侧', color='r')
G.add_node('档案馆', color='b')
G.add_node('篮球场西北路口', color='r')
G.add_node('篮球场东北路口', color='r')
G.add_node('学二十九东北路口', color='r')
G.add_node('学十三西南路口', color='r')
G.add_node('学十三东南路口', color='r')
G.add_node('学四东南路口', color='r')
G.add_node('学一西北路口', color='r')
G.add_node('学一东北路口', color='r')
G.add_node('学二东北路口', color='r')
G.add_node("教四西北路口", color='r')
G.add_node("学一公寓", color='b')
G.add_node('教四北侧', color='r')
G.add_node('学二公寓', color='b')
G.add_node('教四东北路口', color='r')
G.add_node('图书馆', color='b')
G.add_node('办公楼', color='b')
G.add_node('篮球场', color='b')
G.add_node('篮球场西南路口', color='r')
G.add_node('排球场南侧', color='r')
G.add_node('体育馆北侧', color='r')
G.add_node('学二十九公寓', color='b')
G.add_node('邮局', color='b')
G.add_node('教四西南路口', color='r')
G.add_node('教四', color='b')
G.add_node('教四东南路口', color='r')
G.add_node('教一', color='b')
G.add_node('科学会堂西北路口', color='r')
G.add_node('科学会堂', color='b')
G.add_node('体育馆', color='b')
G.add_node('科学会堂东北路口', color='r')
G.add_node('体育场', color='b')
G.add_node('西门', color='r')
G.add_node('校训石', color='r')
G.add_node('主席像东侧', color='r')
G.add_node('停车坪', color='r')
G.add_node('教三', color='b')
G.add_node('教三东北路口', color='r')
G.add_node('主楼', color='b')
G.add_node('教二', color='b')
G.add_node('教二东北路口', color='r')
G.add_node("体育场西侧", color='r')
G.add_node('校车车库', color='r')
G.add_node('中门内', color='r')
G.add_node('教二东南路口', color='r')
G.add_node('创新楼', color='b')
G.add_node('体育场西南路口', color='r')
G.add_node('中门外', color='r')
G.add_node('校医院', color='b')
G.add_node('学十西', color='r')

G.add_edge('酒店', '学11公寓', weight=8)
G.add_edge('学11公寓', '学十西', weight=2)
G.add_edge('学十西', '美团外卖柜', weight=5)
G.add_edge('学十西', '教九', weight=3)
G.add_edge('美团外卖柜', '北门', weight=12)
G.add_edge('北门', '学十东路口', weight=9)
G.add_edge('学十东路口', '综合食堂东北路口', weight=1)
G.add_edge('学十东路口', '经管楼', weight=5)
G.add_edge('综合食堂东北路口', '学十', weight=7)
G.add_edge('综合食堂东北路口', '新食堂', weight=3)
G.add_edge('综合食堂西北路口', '教九', weight=2)
G.add_edge('综合食堂西北路口', '学十', weight=5)
G.add_edge('综合食堂西北路口', '学九和留学生公寓', weight=5)
G.add_edge('经管楼', '综合服务楼北路口', weight=7)
G.add_edge('综合服务楼北路口', '京东快递站南路口', weight=12)
G.add_edge('京东快递站南路口', '学六公寓', weight=5)
G.add_edge('京东快递站南路口', '科研楼', weight=4)
G.add_edge('科研楼', '东北门', weight=16)
G.add_edge('东北门', '学二十九东北路口', weight=15)
G.add_edge('学二十九东北路口', '篮球场东北路口', weight=6)
G.add_edge('篮球场东北路口', '篮球场西北路口', weight=14)
G.add_edge('篮球场东北路口', '体育馆北侧', weight=12)
G.add_edge('体育馆北侧', '排球场南侧', weight=2)
G.add_edge('体育馆北侧', '学二十九公寓', weight=3)
G.add_edge('排球场南侧', '篮球场西南路口', weight=12)
G.add_edge('篮球场西南路口', '篮球场', weight=6)
G.add_edge('篮球场', '篮球场西北路口', weight=6)
G.add_edge('篮球场西北路口', '学苑和老食堂', weight=4)
G.add_edge('学苑和老食堂', '科研楼西路口', weight=4)
G.add_edge('科研楼西路口', '京东快递站南路口', weight=7)
G.add_edge('科研楼西路口', '物美和浴室', weight=9)
G.add_edge('物美和浴室', '学生活动中心南侧', weight=9)
G.add_edge('学生活动中心南侧', '综合食堂东南路口', weight=6)
G.add_edge('综合食堂东南路口', '新食堂', weight=3)
G.add_edge('综合食堂东南路口', '综合食堂西南路口', weight=12)
G.add_edge('综合食堂西南路口', '综合食堂西北路口', weight=6)
G.add_edge('综合食堂西南路口', '学五西北路口', weight=10)
G.add_edge('学五西北路口', '青年公寓', weight=4)
G.add_edge('学五西北路口', '学五西南路口', weight=4)
G.add_edge('学五西南路口', '学五公寓', weight=5)
G.add_edge('学五公寓', '学五东南路口', weight=5)
G.add_edge('学五东南路口', '综合食堂西南路口', weight=4)
G.add_edge('学五东南路口', '学八公寓', weight=5)
G.add_edge('学八公寓', '大电视北路口', weight=7)
G.add_edge('大电视北路口', '综合食堂东南路口', weight=4)
G.add_edge('学五西南路口', '学十三公寓', weight=4)
G.add_edge('学十三公寓', '学三公寓', weight=5)
G.add_edge('学三公寓', '学三东北路口', weight=5)
G.add_edge('学三东北路口', '学五东南路口', weight=4)
G.add_edge('学三东北路口', '学四公寓', weight=5)
G.add_edge('学四公寓', '大电视南路口', weight=7)
G.add_edge('大电视南路口', '大电视北路口', weight=4)
G.add_edge('大电视南路口', '小松林北侧', weight=6)
G.add_edge('小松林北侧', '麦当劳和学生发展中心', weight=4)
G.add_edge('麦当劳和学生发展中心', '学生活动中心南侧', weight=4)
G.add_edge('小松林北侧', '学生发展中心南侧', weight=6)
G.add_edge('学生发展中心南侧', '档案馆', weight=6)
G.add_edge('档案馆', '篮球场西北路口', weight=6)
G.add_edge('学十三公寓', '学十三西南路口', weight=4)
G.add_edge('学十三西南路口', '学十三东南路口', weight=10)
G.add_edge('学十三东南路口', '学三东北路口', weight=4)
G.add_edge('学十三东南路口', '学四东南路口', weight=12)
G.add_edge('学四东南路口', '大电视南路口', weight=4)
G.add_edge('学十三西南路口', '学一西北路口', weight=4)
G.add_edge('学一西北路口', '学一东北路口', weight=10)
G.add_edge('学一东北路口', '学十三东南路口', weight=4)
G.add_edge('学一东北路口', '学二东北路口', weight=12)
G.add_edge('学二东北路口', '学四东南路口', weight=4)
G.add_edge('学一西北路口', '教四西北路口', weight=4)
G.add_edge('教四西北路口', '学一公寓', weight=5)
G.add_edge('学一公寓', '教四北侧', weight=5)
G.add_edge('教四北侧', '学一东北路口', weight=4)
G.add_edge('教四北侧', '学二公寓', weight=6)
G.add_edge('学二公寓', '教四东北路口', weight=6)
G.add_edge('教四东北路口', '学二东北路口', weight=4)
G.add_edge('教四东北路口', '办公楼', weight=12)
G.add_edge('办公楼', '图书馆', weight=6)
G.add_edge('图书馆', '学生发展中心南侧', weight=6)
G.add_edge('办公楼', '篮球场西南路口', weight=12)
G.add_edge('教四西北路口', '邮局', weight=8)
G.add_edge('邮局', '教四西南路口', weight=8)
G.add_edge('教四西南路口', '教四', weight=11)
G.add_edge('教四', '教四东南路口', weight=11)
G.add_edge('教四东南路口', '教四东北路口', weight=16)
G.add_edge('教四东南路口', '教一', weight=12)
G.add_edge('教一', '科学会堂西北路口', weight=12)
G.add_edge('科学会堂西北路口', '篮球场西南路口', weight=16)
G.add_edge('科学会堂西北路口', '科学会堂', weight=6)
G.add_edge('科学会堂', '科学会堂东北路口', weight=6)
G.add_edge('科学会堂东北路口', '体育馆', weight=8)
G.add_edge('体育馆', '排球场南侧', weight=8)
G.add_edge('科学会堂东北路口', '体育场', weight=5)
G.add_edge('教四西南路口', '西门', weight=8)
G.add_edge('西门', '校训石', weight=11)
G.add_edge('校训石', '教四', weight=8)
G.add_edge('校训石', '主席像东侧', weight=11)
G.add_edge('主席像东侧', '教四东南路口', weight=8)
G.add_edge('西门', '停车坪', weight=8)
G.add_edge('停车坪', '教三', weight=11)
G.add_edge('教三', '校训石', weight=8)
G.add_edge('教三', '教三东北路口', weight=11)
G.add_edge('教三东北路口', '主席像东侧', weight=8)
G.add_edge('教三东北路口', '教二', weight=12)
G.add_edge('教二', '主楼', weight=8)
G.add_edge('主楼', '教一', weight=8)
G.add_edge('教二', '教二东北路口', weight=12)
G.add_edge('教二东北路口', '科学会堂西北路口', weight=16)
G.add_edge('教二东北路口', '体育场西侧', weight=12)
G.add_edge('体育场西侧', '科学会堂东北路口', weight=16)
G.add_edge('停车坪', '校车车库', weight=16)
G.add_edge('校车车库', '中门内', weight=22)
G.add_edge('中门内', '教三东北路口', weight=16)
G.add_edge('中门内', '教二东南路口', weight=24)
G.add_edge('教二东南路口', '教二东北路口', weight=16)
G.add_edge('教二东南路口', '创新楼', weight=6)
G.add_edge('创新楼', '体育场西南路口', weight=6)
G.add_edge('体育场西南路口', '体育场西侧', weight=16)
G.add_edge('中门内', '中门外', weight=5)
G.add_edge('中门外', '校医院', weight=10)

# path = nx.shortest_path(G, "教三", "学五公寓", weight="weight")
path = G.shortest_path("图书馆", "学五公寓")
print(path)
# for node in path:
#     print(G.nodes[node]['color'])
