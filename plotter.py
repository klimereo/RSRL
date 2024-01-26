import networkx as nx
import matplotlib.pyplot as plt

# Example data
U_int = {"u1", "u2", "u3", "u4", "u5", "u6", "u7"}
Smax_ass = {("u1", "word"), ("u2", "list"), ("u3", "synsem"), ("u4", "noun"),
            ("u5", "ref-index"), ("u6", "3rd"), ("u7", "sing")}
A_int = {(("u1", "PHON"), "u2"), (("u1", "SYNSEM"), "u3"), (("u3", "CAT"), "u4"),
         (("u3", "CONT"), "u5"), (("u5", "PER"), "u6"), (("u5", "NUM"), "u7") }

root_node = 'word'
# Create a directed graph
G = nx.DiGraph()

# Add nodes with their types
for node, node_type in Smax_ass:
    G.add_node(node, type=node_type)

# Add edges with labels
for (source, label), target in A_int:
    G.add_edge(source, target, label=label)

# Draw the graph
pos=nx.spectral_layout(G)# You can change the layout algorithm as needed
node_types = nx.get_node_attributes(G, 'type')
nx.draw(G, pos, with_labels=False, font_weight='bold', node_color='black', node_size=25, font_size=10, edge_color='gray', arrowsize=12)

# Add node type labels with adjusted position
label_pos = {k: [v[0], v[1] + 0.05] for k, v in pos.items()}  # Adjust the vertical position
nx.draw_networkx_labels(G, label_pos, labels={node: node_types[node] for node in G.nodes}, font_color='black')

# Add edge labels
edge_labels = {(source, target): label for (source, label), target in A_int}
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='red')
print(nx.is_directed_acyclic_graph(G))


# Show the plot
plt.show()
