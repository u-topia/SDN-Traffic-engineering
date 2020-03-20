# 该文档用于生成仿真的流量数据，用于测试模型
# 其中，根据分布随机产生流的目的节点，流长度，开始时间等信息
# 每个节点单独生成需求，两两之间互不影响

import graduation_project.parsers as gp
from gevent import monkey
monkey.patch_all()
import gevent, time
import random
import numpy

global data
data = []
Header = ['发起时间', '源节点', '目的节点', '流长度']
data.append(Header)

# 写成运行的内容
def work(from_node, node_list):
    time_start = time.time()
    while True:
        sec = CreatePoisson(5)   # 泊松分布均值为5
        time.sleep(sec)
        linedata = []
        now = time.strftime("%Y-%m-%d-%H:%M:%S", time.localtime())
        linedata.append(now)
        linedata.append(from_node)
        while True:
            to_node = random.choice(node_list)
            if to_node != from_node:
                break
        linedata.append(to_node)
        flow_len = CreateExponetial(168)
        linedata.append(flow_len)
        data.append(linedata)
        time_end = time.time()
        if time_end - time_start >= 300:
            break

# 多协程运行，生成数据信息
def ManyAssociation(node_list):
    task_list = []
    for from_node in node_list:
        task = gevent.spawn(work, from_node, node_list)
        task_list.append(task)
    gevent.joinall(task_list)

# 将产生的结果写入文件
def write_file(filename, Data):
    with open(filename, 'a', encoding = 'utf-8') as f:
        for row in Data:
            for i in range(len(row)):
                f.writelines(str(row[i]) + '\t\t')
            f.writelines('\n')
    print("写入文件成功")

# 产生服从指数分布的数，用以产生流的长度
def CreateExponetial(a):  # a表示指数分布的参数,一般平均长度为168，最大1514，最小168
    while True:
        exponential = numpy.random.exponential(a)
        if 1514 > exponential >= 42:
            return exponential
    # print(exponential)


# 产生服从泊松分布的数，用以产生流的发生时间
def CreatePoisson(a, n = 1):  # a表示泊松分布的期望，n表示产生的个数
    poisson = numpy.random.poisson(lam = a, size = 1)
    # print(poisson)
    return poisson

def SimulationDataTest():
    a = input('请输入选择的拓扑（B4/IBM）:')
    links, capacity, link_probs, node_list = gp.readTopology(a)
    filename = input('请输入文件名')
    ManyAssociation(node_list)
    write_file(filename, data)

# SimulationDataTest()