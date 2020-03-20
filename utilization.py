# 此文件用于计算网络拓扑中的链路利用率

from graduation_project import parsers

def readFile(filename):
    filename = 'data/' + filename
    file1 = open(filename, 'r', encoding = 'utf-8')
    data = file1.readlines()
    x = []
    for line in data:
        if line == '\n':
            continue
        line_data = line.split()
        x.extend(line_data)
    # print(x)
    data_flow = []
    sum = 0
    flag = 0
    for i in x:
        if 'bf' in i:
            flag = 1
        elif flag == 1:
            data_flow.append(float(i))
            sum += float(i)
            flag = 0
        elif 'Aft' in i:
            break
    return sum, data_flow

def compute_utilization(sum, demand):
    demand_sum = 0
    for i in demand:
        demand_sum += i
    a = sum / demand_sum
    return a


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
    sum, data_flow = readFile(filename)
    a = 'data/' + topology
    links, capacity, link_probs, nodes = parsers.readTopology(a)
    demand, flows = parsers.readDemand(a, len(nodes), 1)
    consequence = compute_utilization(sum, demand)
    print(consequence)

