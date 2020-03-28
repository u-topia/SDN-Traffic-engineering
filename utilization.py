# 该文档用以计算链路利用率
from graduation_project import parsers
from graduation_project import KshortestPaths

def readFile(filename):
    filename = 'data/' + filename
    file1 = open(filename, 'r', encoding='utf-8')
    data = file1.readlines()
    x = []
    for line in data:
        if line == '\n':
            continue
        line_data = line.split()
        x.extend(line_data)
    data_Aft = []
    flag = 0
    for i in x:
        if 'Aft' in i:
            flag = 1
        elif flag == 1:
            flag += 1
        elif flag == 2:
            data_Aft.append(float(i))
            flag = 0
    return data_Aft

def compute_utilization(Ce, Tf, data_Aft):
    sum_Ce = 0
    for i in Ce:
        sum_Ce += i
    sum = 0
    for i in range(len(Tf)):
        sum += len(Tf[i]) * data_Aft[i]
    utilization = sum / sum_Ce
    return utilization


if __name__ == '__main__':
    topology = input('请输入拓扑：')
    arithmetic = input('请输入配置算法：(FFC,TE,TEAVAR)')
    num = input('请输入K最短路径算法的路径数：')
    filename = topology + '-' + arithmetic + '-' + num
    if arithmetic == 'FFC':
        num1 = input('请输入最大容纳错误数：')
        filename = filename +  '-' + num1
    filename = filename +  '.txt'
    print(filename)
    data_Aft = readFile(filename)
    a = 'data/' + topology
    links, capacity, link_probs, nodes = parsers.readTopology(a)
    demand, flows = parsers.readDemand(a, len(nodes), 1)
    dict = KshortestPaths.create_dict(links, nodes)
    # 找到前k条最短路径
    k = int(input('请输入最短路数量：'))
    all_k_shortest_path = KshortestPaths.ksp(dict, nodes, flows, k)
    # all_k_shortest_path = KshortestPaths.solve_path_random(dict, nodes, flows, k)
    # for i in all_k_shortest_path:
    #     print(i)
    Tf = KshortestPaths.solve_path(all_k_shortest_path, flows, links, k)
    consequence = compute_utilization(capacity, Tf, data_Aft)
    print(consequence)