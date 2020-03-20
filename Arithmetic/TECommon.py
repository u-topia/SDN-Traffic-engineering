from graduation_project import parsers
from graduation_project import KshortestPaths
import gurobipy as gp
from gurobipy import GRB

# 基本TE
def TE_Common(Tf, capacity, demand, flows, links, k):
    # 创建一个新模型
    m = gp.Model('test_TE')

    # 创建变量
    # 定义每条流的带宽分配，即代表最大吞吐量
    temp = range(len(flows))
    bf = m.addVars(temp, name='bf')

    # 定义每条tunnel通过的流
    temp1 = range(len(flows) * k)
    Aft = m.addVars(temp1, name='Aft')

    # 设置目标
    expr = sum(bf[i] for i in range(len(flows)))
    m.setObjective(expr, GRB.MAXIMIZE)  # 最大化

    # 设置约束
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

    # 约束条件1
    list4 = range(len(links))
    for i in list4:
        expr2 = sum(L[int(a / k)][a % k][i] * Aft[a] for a in range(k * len(flows)))
        m.addConstr(expr2 <= capacity[i], "c1")

    # 约束条件2
    list2 = range(len(flows))
    for i in list2:
        expr1 = sum(Aft[j] for j in range(i * k, (i + 1) * k))
        m.addConstr(expr1 >= bf[i], "c2")

    # 约束条件3
    list1 = range(len(flows))
    for i in list1:
        m.addConstr(bf[i] <= demand[i], "c3")
        m.addConstr(0 <= bf[i], "c4")

    # 约束条件4 非负约束
    list3 = range(len(flows) * k)
    for i in list3:
        m.addConstr(Aft[i] >= 0, "c5")

    m.optimize()

    for i in range(len(flows)):
        bf[i] = bf[i].X

    for i in range(len(flows) * k):
        Aft[i] = Aft[i].X
    print(bf)
    print(Aft)

    file = 'Arithmetic/' + input('请输入文件名（xxx.lp)')
    m.write(file)

    return bf, Aft

def TestTECommon():
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
    print(Tf)   # Tf保存路径在links中的索引值
    TE_Common(Tf, capacity, demand, flows, links, k)

# TestTECommon()