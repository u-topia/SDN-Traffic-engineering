from graduation_project import parsers
import numpy as np


Inf = float('inf')

# 生成邻接矩阵
def create_matrix(links, nodes):
    a = len(nodes)
    graph = np.zeros((a, a))
    for i in range(a):
        for j in range(a):
            graph[i][j] = float('inf')
            if i == j:
                graph[i][j] = 0
    for i in range(a):
        for j in range(a):
            if (i + 1,j + 1) in links:
                graph[i][j] = 1
    return graph

# 生成邻接表（字典形式）
def create_dict(links, nodes):
    a = len(nodes)
    dict = {}
    for i in range(a):
        dict[nodes[i]] = []
    for i in range(a):
        for j in range(a):
            if (i + 1,j + 1) in links:
                dict[nodes[i]].append(nodes[j])
    print(dict)
    return dict


# 遍历从起点到终点的所有路径
def findAllPath(graph, start, end, path = []):
    path = path + [start]
    if start == end:
        return [path]

    paths = []  # 存储所有路径
    for node in graph[start]:
        if node not in path:
            newpaths = findAllPath(graph, node, end, path)
            for newpath in newpaths:
                paths.append(newpath)
    return paths


# 迪杰斯特拉算法实现
def dijkstra(graph, src, dst, n): #graph表示邻接矩阵，n表示节点数
    src = src - 1
    dst = dst - 1
    dist = [Inf] * n
    dist[src] = 0
    book = [0] * n  # 记录已确定的顶点
    # 每次找到起点到该点的最短路径
    u = src
    for h in range(n - 1):   # 寻找n-1次
        book[u] = 1  # 已经确定记录为1
        # 更新距离并记录最小距离的节点
        next_u, minVal = None, float('inf')
        for v in range(n):
            w = graph[u][v]
            if w == Inf:
                continue
            if not book[v] and dist[u] + w < dist[v]:   # 判断节点是否已经确定了
                dist[v] = dist[u] + w
                if dist[v] < minVal:
                    next_u, minVal = v, dist[v]
        # 开始下一轮遍历
        u = next_u
        print(u)
    print(dist)
    return dist[dst]

# K最短路径算法
def ksp(dict, nodes, flows, k):
    a = len(nodes)
    all_k_shortest_path = []
    for i in range(a):
        for j in range(a):
            if i != j:
                index1 = flows.index((i + 1, j + 1))
                paths = findAllPath(dict, nodes[i], nodes[j])
                for m in range(k):
                    for n in range(m + 1,len(paths)):
                        if(len(paths[m]) > len(paths[n])):
                            r = paths[m]
                            paths[m] = paths[n]
                            paths[n] = r
                all_k_shortest_path.append(paths[:k])
                # print(all_k_shortest_path[index1])
    # print(all_k_shortest_path)
    return all_k_shortest_path

# 路径处理
def solve_path(all_k_shortest_path, flows, links, k):
    Tf = []  # 记录每条路径在flows中的索引值
    for i in range(len(all_k_shortest_path)):
        change = []
        for j in range(len(all_k_shortest_path[i])):
            num = []
            for k in range(len(all_k_shortest_path[i][j]) - 1):
                nodes1 = int(all_k_shortest_path[i][j][k].replace("s",""))
                nodes2 = int(all_k_shortest_path[i][j][k + 1].replace("s", ""))
                # print(str(nodes1) + ' ' + str(nodes2))
                num_flows = links.index((nodes1, nodes2))
                # print(num_flows)
                num.append(num_flows)
                # print(num)
            change.append(num)
        Tf.append(change)
    return Tf


# 算法测试
def test_yen_ksp():
    a = input('请输入选择的拓扑（B4/IBM）:')
    links, capacity, link_probs, nodes = parsers.readTopology(a)

    dict = create_dict(links,nodes)
    # paths = findAllPath(dict, 's1','s3')
    # print(paths)

    demand, flows = parsers.readDemand(a, len(nodes), 1)
    k = int(input('请输入最短路数量：'))
    all_k_shortest_path = ksp(dict, nodes, flows, k)
    for i in all_k_shortest_path:
        print(i)
    Tf = solve_path(all_k_shortest_path, flows, links, k)
    print(Tf)   # Tf保存路径在links中的索引值

# test_yen_ksp()


