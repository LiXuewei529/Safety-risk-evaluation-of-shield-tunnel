knowledge_graph = {
    "Individual Competence": {
        "Safety awareness": ["Violation of regulations", "Inadequate risk response"],
        "Risk assessment skills": ["Failure to identify hazards"],
        "Operational proficiency": ["Cutterhead jamming due to improper operation"]
    },
    "Individual Action": {
        "Violation of regulations": ["Premature removal of support", "Continued excavation in weak soil"],
        "Inadequate risk response": ["Delayed support reinforcement", "Poor emergency handling"],
        "Premature removal of support": ["Insufficient bearing capacity"],
        "Habitual illegal operations": ["Ineffective safety inspections", "Violation of construction principles"]
    },
    "Management System": {
        "Safety management": ["Inadequate training", "Lack of emergency plans"],
        "Risk assessment": ["Overlooked geological risks", "Underestimation of water inrush risks"],
        "Geological exploration": ["Unidentified underground obstacles", "Stratum instability"],
        "Equipment maintenance": ["Cutterhead wear", "Lack of regular checks"],
        "Safety inspection": ["Failure to detect structural issues", "Inadequate monitoring"]
    },
    "Accident Type": {
        "Tunnel collapse": ["Bearing capacity failure", "Structural instability", "Water inrush"],
        "Cutterhead jamming": ["Equipment malfunction", "Operational error"],
        "Water inrush": ["Increased support pressure", "Support structure failure"]
    },
    "Organizational Culture": {
        "Safety culture": ["Inadequate training programs", "Tolerance of violations"],
        "Risk management culture": ["Superficial risk assessments", "Pressure to meet deadlines"]
    },
    "Environmental Factors": {
        "Complex geology": ["Increased excavation risks", "Unforeseen ground conditions"],
        "Water inrush conditions": ["Unexpected water flow", "Increased tunnel instability"]
    },
    "Equipment Conditions": {
        "Support structure integrity": ["Collapse risk", "Insufficient strength"],
        "Cutterhead condition": ["Jamming incidents", "Performance degradation"]
    },
    "Project Pressures": {
        "Schedule adherence": ["Rushed construction", "Compromised safety measures"],
        "Cost constraints": ["Underinvestment in safety", "Use of substandard equipment"]
    },
    "Regulatory Oversight": {
        "Supervision of safety practices": ["Lack of enforcement", "Inadequate penalties for violations"],
        "Geological survey requirements": ["Inadequate pre-construction assessments", "Failure to identify hazards"]
    }
}



import networkx as nx
import matplotlib.pyplot as plt

G = nx.DiGraph()

# Add nodes with categories as colors
node_colors = {
    "Individual Competence": "skyblue",
    "Individual Action": "lightgreen",
    "Management System": "yellow",
    "Accident Type": "red",
    "Organizational Culture": "lightgray"
}

# Create a dictionary to hold the color for each node
node_color_map = {}

# Function to determine the category of a relation if it's not explicitly defined
def get_category(relation, default_category):
    for category, entities in knowledge_graph.items():
        for entity in entities:
            if relation in entities[entity]:
                return category
    return default_category

for category, entities in knowledge_graph.items():
    for entity, relations in entities.items():
        # Assign the color based on the category
        node_color_map[entity] = node_colors[category]
        G.add_node(entity)  # Add node to the graph
        for relation in relations:
            if relation not in node_color_map:  # Add related nodes that might not have been added yet
                node_color_map[relation] = node_colors[get_category(relation, category)]
            G.add_edge(entity, relation)  # Add edge to the graph



# Position the nodes
pos = nx.spring_layout(G)

# Draw the graph
nx.draw(G, pos, with_labels=True, node_color=[node_color_map[node] for node in G.nodes()])
plt.show()