from graduation_project.Arithmetic import FFC
from graduation_project.Arithmetic import TECommon
from graduation_project.Arithmetic import TEAVAR
from graduation_project import parsers
from graduation_project import KshortestPaths

def WriteToFile(filename, bf, Aft, flows, k):
    with open(filename,'w',encoding = 'utf-8') as file1:
        for i in range(len(flows)):
            file1.writelines('bf{:<5}'.format(i))
            file1.writelines('{:<20}'.format(bf[i]))
            file1.writelines('\t\t')
            if (i + 1) % 5 == 0:
                file1.writelines('\n')
        file1.writelines('\n')
        for i in range(len(flows)):
            for j in range(k):
                file1.writelines('Aft{:<3},{:<5}'.format(i + 1,j + 1))
                file1.writelines('{:<20}'.format(Aft[i * k + j]))
                file1.writelines('\t\t')
            file1.writelines('\n')
    print('写入文件完成')

def TestFFC():
    # 读取拓扑信息和需求信息
    a = 'data/' + input('请输入选择的拓扑：（IBM/B4）')
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
    # print(Tf)   # Tf保存路径在links中的索引值
    fault = int(input('请输入最大允许错误数：'))
    bf, Aft = FFC.FFC_arithmetic(Tf, capacity, demand, flows, links, k, fault)
    name = 'data/' + input('请输入要保存的文件名：')
    WriteToFile(name, bf, Aft, flows, k)

def TestTECommon():
    # 读取拓扑信息和需求信息
    a = 'data/' + input('请输入选择的拓扑：（IBM/B4）')
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
    print(Tf)  # Tf保存路径在links中的索引值
    bf, Aft = TECommon.TE_Common(Tf, capacity, demand, flows, links, k)
    name = 'data/' + input('请输入要保存的文件名：')
    WriteToFile(name, bf, Aft, flows, k)

def TestTeaVar():
    # 读取拓扑信息和需求信息
    a = 'data/' + input('请输入选择的拓扑：（IBM/B4）')
    links, capacity, link_probs, nodes = parsers.readTopology(a)
    demand, flows = parsers.readDemand(a, len(nodes), 1)

    dict = KshortestPaths.create_dict(links, nodes)
    # 找到前k条最短路径
    k = int(input('请输入最短路数量：'))
    all_k_shortest_path = KshortestPaths.ksp(dict, nodes, flows, k)
    # for i in all_k_shortest_path:
    #     print(i)
    Tf = KshortestPaths.solve_path(all_k_shortest_path, flows, links, k)
    print(Tf)  # Tf保存路径在links中的索引值
    TEAVAR.TeaVar(links, capacity, demand, flows, Tf, k)
    # print(len(flows))

def TestTECommonDy():
    # 读取拓扑信息和需求信息
    a = 'data/' + input('请输入选择的拓扑：（IBM/B4）')
    links, capacity, link_probs, nodes = parsers.readTopology(a)
    dict = KshortestPaths.create_dict(links, nodes)
    demand, flows = parsers.readDemand(a, len(nodes), 1)
    # 找到前k条最短路径
    k = int(input('请输入最短路数量：'))
    all_k_shortest_path = KshortestPaths.ksp(dict, nodes, flows, k)
    # for i in all_k_shortest_path:
    #     print(i)
    Tf = KshortestPaths.solve_path(all_k_shortest_path, flows, links, k)
    print(Tf)  # Tf保存路径在links中的索引值
    Arithmetic = input('请输入算法选择（FFC，TECommon，TEAVAR)：')
    time = 0
    if Arithmetic == 'TECommon':
        for i in range(10):
            time += 1
            if i == 0:
                demand, flows = parsers.readDemand(a, len(nodes), i + 1)
                # print(difference_value)
            else:
                demand, flows = parsers.readDemand(a, len(nodes), i + 1)
                demand += difference_valus
            difference_valus = [0] * len(flows)
            bf, Aft = TECommon.TE_Common(Tf, capacity, demand, flows, links, k)
            for j in range(len(flows)):
                difference_valus[j] = demand[j] - bf[j]
        i = 0
        while difference_valus != [0] * len(flows):
            if i > 100:
                break
            bf, Aft = TECommon.TE_Common(Tf, capacity, demand, flows, links, k)
            for j in range(len(flows)):
                difference_valus[j] = difference_valus[j] - bf[j]
            time += 1
    elif Arithmetic == 'FFC':
        fault = int(input('请输入最可可允许的错误数：'))
        for i in range(10):
            time += 1
            if i == 0:
                demand, flows = parsers.readDemand(a, len(nodes), i + 1)
                # print(difference_value)
            else:
                demand, flows = parsers.readDemand(a, len(nodes), i + 1)
                demand += difference_valus
            difference_valus = [0] * len(flows)
            bf, Aft = FFC.FFC_arithmetic(Tf, capacity, demand, flows, links, k, fault)
            for j in range(len(flows)):
                difference_valus[j] = demand[j] - bf[j]
        i = 0
        difference = [0] * len(flows)
        while difference_valus != [0] * len(flows):
            i += 1
            if i > 100 or difference_valus == difference:
                break
            bf, Aft = FFC.FFC_arithmetic(Tf, capacity, difference_valus, flows, links, k, fault)
            difference = difference_valus
            for j in range(len(flows)):
                difference_valus[j] = difference_valus[j] - bf[j]
            time += 1
        print(difference_valus)
    return time

# TestFFC()
# TestTECommon()
# TestTeaVar()

if __name__ == '__main__':
    time = TestTECommonDy()
    print(time)