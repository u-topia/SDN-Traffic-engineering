import networkx as nx
import matplotlib.pyplot as plt
from graduation_project import parsers

def draw_topology():
    # 读取拓扑信息和需求信息
    a = '../data/' + input('请输入选择的拓扑：（IBM/B4）')
    links, capacity, link_probs, nodes = parsers.readTopology(a)
    links_new = []
    for i in links:
        a = 's' + str(i[0])
        b = 's' + str(i[1])
        links_new.append((a,b))
    # print(links_new)

    G = nx.Graph()
    for node in nodes:
        G.add_node(node)

    G.add_edges_from(links_new)

    nx.draw(G, with_labels=True)
    a = input('请输入文件名')
    plt.savefig(a)
    plt.show()

def draw_statistical_chart():
    return

# draw_topology()