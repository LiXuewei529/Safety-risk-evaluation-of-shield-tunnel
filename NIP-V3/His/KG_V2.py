

import json

data_file = '../Data/knowledge_graph_V3.json'
# data_file = './Data/knowledge_graph_V2.json'

# 从文件中读取JSON数据
with open(data_file, 'r', encoding='utf-8') as file:
    knowledge_graph = json.load(file)

print("知识图谱数据已成功读取：")
print(knowledge_graph)



import networkx as nx
import matplotlib.pyplot as plt
from networkx.drawing.nx_agraph import graphviz_layout
import numpy as np



# knowledge_graph_V3
category_colors = {
    "Safety Culture": "lightyellow",
    "Safety Management System": "lightpink",
    "Habitual Behaviors": "lightgreen",
    "One-time behavior and physical conditions": "lightblue",
    "Accident Type": "red",
}

# Define colors for different categories
# category_colors = {
#     "Organizational Culture": "lightblue",
#     "Management System": "lightgreen",
#     "Habitual Behaviors": "lightpink",
#     "One-time Actions and States": "lightyellow",
#     "Accident Type": "red",
# }








# 创建有向图
G = nx.DiGraph()

# 添加节点及颜色
node_sizes = []
node_colors = []
for category, entities in knowledge_graph.items():
    for entity, evolutions in entities.items():
        G.add_node(entity, label=entity.replace(' ', '\n'))
        node_colors.append(category_colors[category])
        node_sizes.append(4000 + 40 * len(entity))  # 根据文字长度调整节点大小

# 添加边并计算权重
for category, entities in knowledge_graph.items():
    for entity, evolutions in entities.items():
        if evolutions:
            weight_base = np.random.rand(len(evolutions))  # 生成随机基础权重
            weights = weight_base / weight_base.sum()  # 归一化权重
            for evolution, weight in zip(evolutions, weights):
                G.add_edge(entity, evolution, weight=weight, label=f"{weight:.2f}")

# 使用Graphviz布局
plt.figure(figsize=(24, 20))
pos = graphviz_layout(G, prog='dot')

# 绘制节点
nodes = nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=node_sizes, alpha=0.9)
nodes.set_edgecolor('black')  # 节点边框

# 绘制边和权重标签，使用fancy箭头样式和arc3连接样式
# 绘制边和权重标签
edges = nx.draw_networkx_edges(
    G, pos,
    edgelist=G.edges(),
    arrowstyle='-|>',
    arrowsize=15,  # 增大箭头尺寸以提高可见性
    edge_color='gray',
    width=[G[u][v]['weight']*5 for u, v in G.edges()],
    connectionstyle='arc3,rad=0.1',
    min_target_margin=30  # 设置箭头与目标节点的最小距离
)
edge_labels = nx.get_edge_attributes(G, 'label')
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='red')

# 绘制节点标签
labels = nx.get_node_attributes(G, 'label')
nx.draw_networkx_labels(G, pos, labels, font_size=9, font_family="sans-serif")

# 添加图例
categories = category_colors.keys()
plt.legend([plt.Line2D([0], [0], color=color, marker='o', linestyle='') for color in category_colors.values()], categories, title="Categories")

plt.title("Evolutionary Knowledge Graph of Construction Risks")
plt.axis('off')  # 关闭坐标轴
plt.savefig('./KG.png')
# plt.show()