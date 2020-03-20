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

# TestFFC()
# TestTECommon()
# TestTeaVar()