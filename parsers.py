# 该文件用于读入输入的拓扑和需求信息
import numpy as np
import math
import networkx as nx
# import diGraph

# 读取拓扑信息
def readTopology(topology,zeroindex = False, downscale = 1):
    urlTopology = topology + '/topology.txt'
    urlNodes = topology + '/nodes.txt'
    input_topology = np.loadtxt(urlTopology,dtype = float,skiprows = (1))    # 读取文件中拓扑信息，容量和错误率
    input_nodes = np.loadtxt(urlNodes,dtype = str,skiprows = (1))
    topology_list = input_topology.tolist()
    nodes_list = input_nodes.tolist()
    # print(nodes_list)
    fromNodes = []
    toNodes = []
    capacity = []
    probabilities = []
    ignore = ()   # 建立一个元组
    links = []
    for row in topology_list:
        fromNodes.append(row[0])
        toNodes.append(row[1])
        capacity.append(row[2] / downscale / 1000)   # 将链路容量的值缩小1000倍
        probabilities.append(row[3])
        # print(row)
    for i in range(len(fromNodes)):
        if((fromNodes[i] not in ignore) and (toNodes[i] not in ignore)):
            con = (int(fromNodes[i] + zeroindex),int(toNodes[i] + zeroindex))
            links.append(con)
    return links,capacity,probabilities,nodes_list

# 矩阵分析
def ParseMatrix(filename,num_nodes,num_demand):
    # num_demand表示指定行的需求,num_nodes表示该拓扑中节点数
    ignore = ()
    start_range = 0
    Inf = float('inf')
    end_range = Inf
    x = np.loadtxt(filename)[num_demand - 1,:]    # 读取指定行的流量需求
    # print(x)
    m = np.ones((len(x) - int(math.sqrt(len(x))),3)) * 0
    # print(m)
    # print(len(x) - int(math.sqrt(len(x))))  # ?
    # print(len(x))
    fromNode = 0
    count = 0
    for i in range(int(math.pow(num_nodes,2) - 1)):
        toNode = i % num_nodes + 1
        if toNode == 1:
            fromNode += 1
        if (fromNode != toNode and i >= start_range and i < end_range and not(fromNode in ignore) and not(toNode in ignore)):
            m[count][0] = fromNode
            m[count][1] = toNode
            m[count][2] = x[i]
            count += 1
    ret = m
    # print(ret)
    for row in range(m.shape[0] - 1,0,-1):
        if(m[row][2] == 0):
            ret = np.delete(ret,row,axis = 0)
    return ret

# topolopy = input('please input topolopy:')
# x,b,c,d = readTopology(topolopy)
# nodes_num = len(d)
# ret = ParseMatrix(topolopy+'/demand.txt',nodes_num,1)
# print(ret)

# 读取需求矩阵信息
# 需求信息不是矩阵时的读入
def IgnoreCycles(demand, zeroindex = False):
    z = [0,0,0]
    for row in range(demand.shape[0]):
        if demand[row][1] != demand[row][2]:
            z = z

def readDemand(filename,num_nodes,num_demand,scale = 1.0,matrix = True,downscale = 1,sigfigs = 1,zeroindex = False):
    fromNodes = []
    toNodes = []
    demand = []
    flows = []
    if matrix:
        input_demand = ParseMatrix(filename + '/demand.txt', num_nodes, num_demand)
    else:
        input_demand = IgnoreCycles(filename + '/demand/' + str(num_nodes) + '.txt' , zeroindex = zeroindex)

    for i in range(input_demand.shape[0]):
        fromNodes.append(int(input_demand[i][0]))
        toNodes.append(int(input_demand[i][1]))
        flows.append((int(input_demand[i][0]),int(input_demand[i][1])))
        demand.append(input_demand[i][2] / downscale * scale / 1000.0)
    return demand, flows

# demand, flows = readDemand('IBM',17,1)
# print(demand)
# print(flows)

# 分析路径
def parsePaths(filename, links, flows, zeroindex = False):
    nflows = len(flows)
    file1 = open(filename,'r',encoding = 'utf-8')
    x = []
    my_data = file1.readlines()
    for line in my_data:
        if line == "\n":
            continue
        line_data = line.split()
        x.append(line_data)
    T = []     # T保存至为每条tunnel所经过的link值
    Tf = []    # 保存的值为：键值为flows的索引，元素为所使用通道在T中的索引值
    for i in range(nflows):
        Tf.append([])
    # print(Tf)
    tf = []
    fromNode = 0
    toNode = 0
    num_flow = -1
    tindex = 0    # 表示t的索引位置
    max_paths = 0
    paths = []
    for i in range(nflows):
        path = []
        for j in range(nflows):
            path.append(np.nan)
        paths.append(path)
    # for i in paths:
    #    print(i)
    for row in range(len(x)):
        if "->" in x[row]:    # 解析从a到b形式的
            max_paths = max(max_paths, len(tf))   # 表示从a到b最多的通路数
            if fromNode != 0 and num_flow != -1:
                paths[fromNode - 1][toNode - 1] = tf
                Tf[num_flow] = tf
            if x[row][0].isdigit():   # 判断是否是一个数字
                fromNode = x[row][0] + zeroindex
                toNode = x[row][2] + zeroindex
            else:
                fromNode = int(x[row][0].replace("h","")) + zeroindex
                toNode = int(x[row][2].replace("h","")) + zeroindex
            try:
                num_flow = flows.index((fromNode,toNode))
            except:
                num_flow = -1
            # print(num_flow)
            tf = []
        else:   # 解析每条路径所通过的link
            t = []
            for col in range(1,len(x[row])):
                if x[row][col].find("]") >= 0:
                    # print(1)
                    break
                r = x[row][col][1:- 2].replace("s","")
                stringtup = r.split(",")
                # 在边缘矩阵中找到边缘
                e = (int(stringtup[0]) + zeroindex, int(stringtup[1]) + zeroindex)
                index = links.index(e)
                t.append(index)
            # 创建新的隧道并且添加到流隧道中
            if num_flow != -1:
                T.append(t)
                tf.append(tindex)
                tindex += 1
            # print(tf)

    # 添加最后一个tunnel
    if num_flow != -1:
        Tf[num_flow] = tf
        paths[fromNode - 1][toNode - 1] = tf
    T.append([])

    for f in range(len(Tf)):
        for t in range(max_paths):
            try:
                abc = Tf[f][t]
            except:
                Tf[f].append(tindex)
    # print(paths)
    return T, Tf, max_paths

# 获得分配，配置
def parseYatesSplittingRatos(filename, k, flows, zeroindex = False):    # 分配比例
    file1 = open(filename, 'r', encoding='utf-8')
    f = []
    my_data = file1.readlines()
    for line in my_data:
        if line == "\n":
            continue
        line_data = line.split()
        f.append(line_data)
    a = np.ones((len(flows),k)) * 0    # 存放着对应flows中路径分配的比例
    num_flow = 0
    t = 0
    for row in range(len(f)):
        if "->" in f[row]:
            fromNode = int(f[row][0].replace("h","")) + zeroindex
            toNode = int(f[row][2].replace("h","")) + zeroindex
            try:
                num_flow = flows.index((fromNode,toNode))
            except:
                num_flow = -1
            t = 0
        else:
            for col in range(len(f[row])):
                if f[row][col].find("@") >= 0:
                    # print(f[row][col + 1])
                    a[num_flow, t] = (math.ceil(float(f[row][col + 1]) * 1000)) / 1000
                    # print(a[num_flow, t])
                    t += 1
                    break
    return a

def parseYatesAllocation(filename, k, demand, flows, zeroindex = False):   # 分配流量
    file1 = open(filename, 'r', encoding='utf-8')
    f = []
    my_data = file1.readlines()
    for line in my_data:
        if line == "\n":
            continue
        line_data = line.split()
        f.append(line_data)
    a = np.ones((len(flows), k)) * 0  # 存放着对应flows中路径分配的比例
    num_flow = 0
    t = 0
    for row in range(len(f)):
        if "->" in f[row]:
            fromNode = int(f[row][0].replace("h", "")) + zeroindex
            toNode = int(f[row][2].replace("h", "")) + zeroindex
            try:
                num_flow = flows.index((fromNode, toNode))
            except:
                num_flow = -1
            t = 0
        else:
            for col in range(len(f[row])):
                if f[row][col].find("@") >= 0:
                    # print(f[row][col + 1])
                    a[num_flow, t] = math.ceil(float(f[row][col + 1]) * demand[num_flow] * 1000) / 1000
                    # print(a[num_flow, t])
                    t += 1
                    break
    return a

# KSP隧道
def getTunnels(nodes, edges, capacity, flows, k = 12, edge_disjoint = False):
    num_edges = len(edges)
    num_nodes = len(nodes)
    num_flows = len(flows)
    graph = nx.DiGraph()
    for node in nodes:
        graph.add_node(node)
    distances = float('inf') * np.ones(num_nodes, num_nodes)

    for i in range(num_edges):
        graph.add_edge_from(edges[i])
        distances[edges[i][1]][edges[i][2]] = 1
        distances[edges[i][2]][edges[i][1]] = 1
    T = [[]]
    Tf = []
    ti = 2
    max_k = 1
    for f in range(num_flows):
        tf = []
        curr_k = 0


def testparsePath():
    a = 'data/' + input('请输入topology：')
    links, capacity, link_probs, nodes = readTopology(a)
    print('links')
    print(links)
    print()
    print('nodes')
    print(nodes)
    print()
    demand, flows = readDemand(a, len(nodes), 1)
    print('flows')
    print(flows)
    print()
    b = input('请输入配置方式：')
    T, Tf, k = parsePaths(a + "/paths/" + b, links, flows)   # 分析路径
    con = parseYatesSplittingRatos(a + "/paths/" + b, k, flows)
    con1 = parseYatesAllocation(a + "/paths/" + b, k, demand, flows)
    print("T:")
    print(T)
    print("Tf:")
    print(Tf)
    print("max_paths:")
    print(k)
    # print(Tf[119])

# testparsePath()