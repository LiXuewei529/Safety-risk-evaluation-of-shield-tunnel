import json
from collections import defaultdict

def load_data(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data

def check_entities(data):
    category_map = defaultdict(list)
    entity_connections = defaultdict(set)
    all_entities = set()

    # 遍历数据，填充category_map和entity_connections
    for category, entities in data.items():
        for entity, targets in entities.items():
            all_entities.add(entity)
            category_map[entity].append(category)
            for target in targets:
                target_entity = target['entity']
                weight = target['weight']
                all_entities.add(target_entity)
                entity_connections[entity].add((target_entity, weight))
                entity_connections[target_entity].add((entity, weight))

    # 检查每个实体是否都有归属的类别
    no_category_entities = [entity for entity in all_entities if entity not in category_map]

    # 检查每个实体是否都只有一种类别
    multi_category_entities = {entity: categories for entity, categories in category_map.items() if len(categories) > 1}

    # 检查每个实体是否都有关系连接
    independent_entities = [entity for entity in all_entities if len(entity_connections[entity]) == 0]

    return no_category_entities, multi_category_entities, independent_entities, len(all_entities), len(data)

def main():
    file_path = 'fig1.json'
    data = load_data(file_path)

    no_category_entities, multi_category_entities, independent_entities, total_entities, total_categories = check_entities(data)

    print(f"Total number of entities: {total_entities}")
    print(f"Total number of categories: {total_categories}")

    if no_category_entities:
        print("Entities with no category:", no_category_entities)
    else:
        print("All entities have a category.")

    if multi_category_entities:
        print("Entities with multiple categories:", multi_category_entities)
    else:
        print("No entity has multiple categories.")

    if independent_entities:
        print("Independent entities with no connections:", independent_entities)
    else:
        print("All entities are connected in some way.")

if __name__ == "__main__":
    main()
