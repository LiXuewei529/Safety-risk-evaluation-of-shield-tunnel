import json
from py2neo import Graph, Node, Relationship
from py2neo.matching import NodeMatcher

# Neo4j 连接配置
NEO4J_URL = 'http://localhost:7474/'
NEO4J_USER = 'neo4j'
NEO4J_PASSWORD = '1'

# 数据文件路径
DATA_FILE = 'Data/V3/knowledge.json'

# 定义类别颜色（可选，作为节点属性存储）
CATEGORY_COLORS = {
    "Safety Culture": "#ffdce8",
    "Safety Management System": "#bcd6eb",
    "Habitual Behaviors": "#f6bdc9",
    "One-time behavior and physical conditions": "#c0dbce",
    "Accident Type": "red",
}


def load_knowledge_graph(data_file):
    """从JSON文件中加载知识图谱数据"""
    with open(data_file, 'r', encoding='utf-8') as file:
        knowledge_graph = json.load(file)
    print("知识图谱数据已成功读取。")
    return knowledge_graph


def connect_neo4j(url, user, password):
    """连接到Neo4j数据库"""
    graph = Graph(url, auth=(user, password))
    print("已连接到Neo4j数据库。")
    return graph


def clear_graph(graph):
    """清空Neo4j数据库中的所有数据"""
    graph.delete_all()
    print("已清空Neo4j数据库中的所有数据。")


def create_nodes(graph, knowledge_graph, category_colors):
    """
    创建节点并设置属性。
    每个类别作为一个独立的标签，并根据类别分配颜色。
    """
    matcher = NodeMatcher(graph)
    for category, entities in knowledge_graph.items():
        color = category_colors.get(category, "#ffffff")  # 默认颜色为白色
        for entity in entities:
            # 检查节点是否已存在，避免重复创建
            existing_node = matcher.match(labels=category, name=entity).first()
            if not existing_node:
                node = Node(category, name=entity, color=color, size=25)
                graph.create(node)
    print("节点创建完成。")


def create_relationships(graph, knowledge_graph):
    """
    创建带有权重的关系。
    关系类型统一为 "RELATED_TO"，并在关系属性中存储权重。
    """
    matcher = NodeMatcher(graph)
    relationships_created = 0
    for category, entities in knowledge_graph.items():
        for entity, targets in entities.items():
            # 找到源节点，使用特定类别标签
            source_node = matcher.match(category, name=entity).first()
            if not source_node:
                continue  # 如果源节点不存在，则跳过

            for target in targets:
                target_entity = target['entity']
                weight = target['weight']

                # 找到目标节点，忽略标签
                target_node = matcher.match(name=target_entity).first()
                if not target_node:
                    # 如果目标节点不存在，先创建它，使用默认标签 "Unknown"
                    target_node = Node("Unknown", name=target_entity, color="#ffffff", size=25)
                    graph.create(target_node)

                # 创建关系，并将权重作为属性存储
                rel = Relationship(source_node, "RELATED_TO", target_node, weight=weight)
                graph.create(rel)
                relationships_created += 1

    print(f"关系创建完成，共创建了 {relationships_created} 条关系。")


def main():
    # 加载知识图谱数据
    knowledge_graph = load_knowledge_graph(DATA_FILE)

    # 连接到Neo4j
    graph = connect_neo4j(NEO4J_URL, NEO4J_USER, NEO4J_PASSWORD)

    # 清空现有数据
    clear_graph(graph)

    # 创建节点
    create_nodes(graph, knowledge_graph, CATEGORY_COLORS)

    # 创建关系
    create_relationships(graph, knowledge_graph)

    print("知识图谱已成功导入到Neo4j。您可以使用Neo4j Browser进行可视化。")


if __name__ == "__main__":
    main()
