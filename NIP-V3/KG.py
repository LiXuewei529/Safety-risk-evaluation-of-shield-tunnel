import json
# from adjustText import adjust_text

data_file = 'Data/V3/knowledge.json'

# 从文件中读取JSON数据
with open(data_file, 'r', encoding='utf-8') as file:
    knowledge_graph = json.load(file)

print("知识图谱数据已成功读取：")
print(knowledge_graph)

import networkx as nx
import matplotlib.pyplot as plt
from networkx.drawing.nx_agraph import graphviz_layout
import numpy as np

# Define colors for different categories

# knowledge_graph_V3
category_colors = {
    "Safety Culture": "lightyellow",
    "Safety Management System": "lightpink",
    "Habitual Behaviors": "lightgreen",
    "One-time behavior and physical conditions": "lightblue",
    "Accident Type": "red",
}

# knowledge_graph_V2
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
node_size = 6000  # 固定节点大小
node_colors = []
for category, entities in knowledge_graph.items():
    for entity, evolutions in entities.items():
        G.add_node(entity, label=entity.replace(' ', '\n'))
        node_colors.append(category_colors[category])

# 添加边并计算权重
for category, entities in knowledge_graph.items():
    for entity, evolutions in entities.items():
        if evolutions:
            # 使用均值为1/n方差为0.01的正态分布来生成扰动
            n = len(evolutions)
            base_weight = 1.0 / n
            perturbation = np.random.normal(0, 0.01, n)  # 生成扰动
            weights = base_weight + perturbation
            weights = np.clip(weights, 0.01, 0.99)  # 确保权重在合理范围内
            weights /= weights.sum()  # 归一化权重以确保总和为1

            for evolution, weight in zip(evolutions, weights):
                G.add_edge(entity, evolution, weight=weight, label=f"{weight:.2f}")

            # 增加跳跃关系
            for i, evolution in enumerate(evolutions):
                for j in range(i + 2, len(evolutions)):  # 跳过一个节点创建跳跃关系
                    jump_weight = np.random.uniform(0.05, 0.15)  # 随机生成跳跃关系的权重
                    G.add_edge(entity, evolutions[j], weight=jump_weight, label=f"{jump_weight:.2f}")

# 确保直接关系链的复杂性
for u, v in list(G.edges()):
    if G[u][v]['weight'] == 1.0:
        G[u][v]['weight'] = np.random.uniform(0.8, 0.99)  # 随机调整直接权重关系
        G[u][v]['label'] = f"{G[u][v]['weight']:.2f}"
        for successor in G.successors(v):
            if G[v][successor]['weight'] == 1.0:
                G[v][successor]['weight'] = np.random.uniform(0.7, 0.9)  # 随机调整后续权重关系
                G[v][successor]['label'] = f"{G[v][successor]['weight']:.2f}"
                jump_weight = np.random.uniform(0.05, 0.15)
                G.add_edge(u, successor, weight=jump_weight, label=f"{jump_weight:.2f}")  # 增加跳跃关系


plt.figure(figsize=(28, 21))
# plt.figure(figsize=(20, 15))
# 使用紧凑布局减少空白
plt.tight_layout()


# 使用Graphviz布局，确保"Accident Type"在中心并调整间距
# 使用原始节点名称作为根节点，调整节点间距
pos = graphviz_layout(G, prog='twopi',
                      args='-Groot="Shield Tunnel Collapse" -Goverlap=false -Gsplines=true -Gscale=2 -Grankdir=LR',
                      )

# 使用spring_layout并调整参数增加节点间距
# pos = nx.spring_layout(G, k=0.4, iterations=10, seed=42)  # k值控制节点间距，iterations控制迭代次数

# 如果希望使用Graphviz的sfdp布局，可以这样设置
# pos = graphviz_layout(G, prog='sfdp', args='-Goverlap=prism -Gsep=1.0 -Gscale=3 -Ginertia=0.5')

# 使用Kamanda-Kawai布局替换twopi布局，适合减少节点重叠
# pos = nx.kamada_kawai_layout(G, )


# 绘制节点
nodes = nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=node_size, alpha=0.9)
nodes.set_edgecolor('black')  # 节点边框

# 绘制边和权重标签
edges = nx.draw_networkx_edges(
    G, pos,
    edgelist=G.edges(),
    arrowstyle='-|>',
    arrowsize=20,  # 增大箭头尺寸以提高可见性
    edge_color='gray',
    width=2,  # 固定边的宽度
    connectionstyle='arc3,rad=0.01',
    min_target_margin=40  # 设置箭头与目标节点的最小距离
)

# 调整权重标签位置
edge_labels = nx.get_edge_attributes(G, 'label')
nx.draw_networkx_edge_labels(
    G, pos,
    edge_labels=edge_labels,
    font_color='red',
    label_pos=0.5,  # 标签居中
    font_size=10,
    font_family="Times New Roman",  # 指定字体
    bbox=dict(facecolor='white', edgecolor='none', pad=0.5)  # 增加背景框以提高可读性
)

# 绘制节点标签时使用adjust_text来自动调整文本位置
labels = nx.get_node_attributes(G, 'label')
texts = []
for node, (x, y) in pos.items():
    texts.append(plt.text(x, y, labels[node], fontsize=12, fontfamily="Times New Roman",
                          verticalalignment='center', horizontalalignment='center'))

# 自动调整文本以防止重叠
# adjust_text(texts, arrowprops=dict(arrowstyle='-', color='gray'))

# 添加图例并旋转
categories = category_colors.keys()
legend = plt.legend(
    [plt.Line2D([0], [0], color=color, marker='o', linestyle='') for color in category_colors.values()],
    categories, title="Categories", loc='center', bbox_to_anchor=(1, 1)
)

# 添加图例并旋转，使用Times New Roman字体
for text in legend.get_texts():
    text.set_fontname('Times New Roman')  # 设置图例文本的字体为Times New Roman
legend.get_title().set_fontname('Times New Roman')  # 设置图例标题的字体为Times New Roman

# for text in legend.get_texts():
#     text.set_rotation(90)
# legend.get_title().set_rotation(90)  # 旋转图例标题

# 设置标题并旋转
# plt.title("Evolutionary Knowledge Graph of Construction Risks", rotation=90, verticalalignment='bottom')

# # 交换x和y轴的显示来旋转整个图像
# ax = plt.gca()
# # 旋转整个图像
# plt.gca().set_aspect('equal', adjustable='box')
# plt.gca().invert_yaxis()
# plt.gca().set_xlim(plt.gca().get_xlim()[::-1])
# plt.gca().set_ylim(plt.gca().get_ylim()[::-1])

plt.axis('off')  # 关闭坐标轴
plt.savefig('./KG.png')
# plt.show()
