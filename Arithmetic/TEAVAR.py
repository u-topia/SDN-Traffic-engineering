import gurobipy as gp
from gurobipy import GRB
from graduation_project import parsers
from graduation_project import KshortestPaths
import numpy as np

def TeaVar(links, capacity, demand, flows, Tf, k, beta, scenarios, scenario_porbs,
           explain = False, verbose = False, utilization = False, average = False):
    nlinks = len(links)
    nflows = len(flows)
    ntunnels = 0
    for i in range(len(Tf)):
        for j in range(len(Tf[i])):
            ntunnels += 1
    # print(ntunnels)
    nscenarios = len(scenarios)
    p = scenario_porbs

    # 生成隧道方案矩阵
    X = np.ones(nscenarios, ntunnels)
    for s in range(nscenarios):
        num = 0
        for i in range(len(Tf)):
            for j in range(len(Tf[i])):
                num += 1
                if len(Tf[i][j]) == 0:
                    X[s][num] = 0
                else:
                    for e in range(nlinks):
                        if scenarios[s][e] == 0:
                            back_edge = links.index((links[e][1],links[e][0]))
                            if e in Tf[i][j] or back_edge in Tf[i][j]:
                                X[s][num] = 0

    # 创建隧道边缘矩阵
        # 处理每条tunnel经过的链路e，L[t, e]
        L = []
        for i in range(len(flows)):
            b = []
            for j in range(k):
                a = []
                for x in range(len(links)):
                    a.append(0)
                b.append(a)
            L.append(b)  # 初始化L矩阵
        # print(L)

        # 设置L表示每条tunnel通过的links
        for i in range(len(flows)):
            for j in range(k):
                for x in range(len(Tf[i][j])):
                    L[i][j][Tf[i][j][x]] = 1
        # for i in range(len(flows)):
        #     for j in range(k):
        #         print(L[i][j])

    # 建立模型
    m = gp.model('TEAVAR')

    # 创建变量
    # 定义alpha
    alpha = m.addVar(name='alpha')

    # 定义Aft，表示每条tunnel通过的流
    temp1 = range(nflows * k)
    Aft = m.addVars(temp1, name='Aft')

    # 定义umax
    temp2 = range(nscenarios)
    umax = m.addVars(temp2, name='umax')

    # 定义u
    temp3 = range(nscenarios * nflows)
    u = m.addVars(temp3, name='u')

    # 设置目标
    expr = sum((p[s] * umax[s]) for s in range(nscenarios))
    m.setObjective(alpha + (1 / (1 - beta)) * expr,GRB.MINIMIZE)

    # 设置约束
    # 约束条件1
    list1 = range(len(links))
    for i in list1:
        expr2 = sum(L[int(a / k)][a % k][i] * Aft[a] for a in range(k * len(flows)))
        m.addConstr(expr2 <= capacity[i], "c1")

    # 约束条件2,非负约束
    for i in range(nscenarios):
        m.addConstr(p[s] >= 0, "c2")

    # 约束条件3
    for s in range(nscenarios):
        for f in range(nflows):
            m.addConstr(umax)

def TEAVARTest():
    # 读取拓扑信息和需求信息
    a = input('请输入选择的拓扑：（IBM/B4）')
    links, capacity, link_probs, nodes = parsers.readTopology(a)
    demand, flows = parsers.readDemand(a, len(nodes), 1)

    dict = KshortestPaths.create_dict(links, nodes)
    # 找到前k条最短路径
    k = int(input('请输入最短路数量：'))
    all_k_shortest_path = KshortestPaths.ksp(dict, nodes, flows, k)
    # for i in all_k_shortest_path:
    #     print(i)
    Tf = KshortestPaths.solve_path(all_k_shortest_path, flows, links, k)
    # print(Tf)   # Tf保存路径在links中的索引值
    TeaVar(links, capacity, demand, flows, Tf, k)