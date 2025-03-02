import json
import jinja2
import numpy as np
from pyvis.network import Network

data_file = 'Data/knowledge_graph_V3.json'

# 从文件中读取JSON数据
with open(data_file, 'r', encoding='utf-8') as file:
    knowledge_graph = json.load(file)

print("知识图谱数据已成功读取：")
print(knowledge_graph)

# Define colors for different categories
category_colors = {
    "Safety Culture": "#ffdce8",
    "Safety Management System": "#bcd6eb",
    "Habitual Behaviors": "#f6bdc9",
    "One-time behavior and physical conditions": "#c0dbce",
    "Accident Type": "red",
}

# 创建Pyvis网络
net = Network(height="1000px", width="100%", directed=True)

# 设置全局样式
net.font = {
    "face": "Times New Roman",
    "color": "black"
}

# 添加节点及颜色
node_size = 25  # 设置节点大小
for category, entities in knowledge_graph.items():
    for entity, evolutions in entities.items():
        # 插入换行符以手动控制标签
        label = "\n".join(entity.split(' '))
        net.add_node(entity, label=label, color=category_colors[category], title=entity, size=node_size)

# 添加边并计算权重，设置权重文字大小
edge_font_size = 8  # 设置边的权重文字大小
added_edges = set()  # 用于跟踪已添加的边
fixed_edge_width = 2  # 固定边的宽度
for category, entities in knowledge_graph.items():
    for entity, evolutions in entities.items():
        if evolutions:
            n = len(evolutions)
            base_weight = 1.0 / n
            perturbation = np.random.normal(0, 0.01, n)
            weights = base_weight + perturbation
            weights = np.clip(weights, 0.01, 0.99)
            weights /= weights.sum()

            for evolution, weight in zip(evolutions, weights):
                if (entity, evolution) not in added_edges:
                    net.add_edge(entity, evolution, value=fixed_edge_width, width=fixed_edge_width, label=f"{weight:.2f}", font={'size': edge_font_size})
                    added_edges.add((entity, evolution))

            for i, evolution in enumerate(evolutions):
                for j in range(i + 2, len(evolutions)):
                    jump_weight = np.random.uniform(0.05, 0.15)
                    if (entity, evolutions[j]) not in added_edges:
                        net.add_edge(entity, evolutions[j], value=fixed_edge_width, width=fixed_edge_width, label=f"{jump_weight:.2f}", font={'size': edge_font_size})
                        added_edges.add((entity, evolutions[j]))

# 确保直接关系链的复杂性
for edge in net.edges:
    u = edge['from']
    v = edge['to']
    if edge['value'] == 1.0:
        edge['value'] = np.random.uniform(0.8, 0.99)
        edge['label'] = f"{edge['value']:.2f}"
        for successor in net.get_adj_list()[v]:
            for succ_edge in net.edges:
                if succ_edge['from'] == v and succ_edge['to'] == successor:
                    if succ_edge['value'] == 1.0:
                        succ_edge['value'] = np.random.uniform(0.7, 0.9)
                        succ_edge['label'] = f"{succ_edge['value']:.2f}"
                        jump_weight = np.random.uniform(0.05, 0.15)
                        if (u, successor) not in added_edges:
                            net.add_edge(u, successor, value=fixed_edge_width, width=fixed_edge_width, label=f"{jump_weight:.2f}")
                            added_edges.add((u, successor))




# 生成并显示可视化
net.show_buttons(filter_=['physics'])  # 添加交互按钮

# 确保在调用show方法之前没有对net.html进行任何修改
net.show("knowledge_graph.html", notebook=False)
