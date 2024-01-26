import random
import networkx as nx

from rsrl import Signatures
from rsrl import Descriptions
from rsrl import Interpretations

# Instantiating the objects
signature = Signatures()
interpretation = Interpretations()
descriptions = Descriptions()

# Reading the signature (ontology)
signature.load_from_json("grammar/signature.json")

# Checking whether the signature is well-formed (sort-resolved, well-typed etc.)
signature.is_partialorder(signature.sorts, signature.hierarchy)
signature.is_appropriate(signature.sorts,
                           signature.hierarchy,
                           signature.attribute_symbols,
                           signature.sort_attributes)
signature.check_rels(signature.relation_symbols, signature.arities)

# Deriving the species
signature.species.update(signature.extract_species(signature.sorts, signature.hierarchy))


# Reading the interpretation

interpretation.load_from_json("grammar/interpretation.json")

interpretation.is_valid_interpretation(signature.attribute_symbols,
                                       signature.sort_attributes,
                                       signature.species,
                                       interpretation.universe,
                                       interpretation.species_assignments,
                                       interpretation.attribute_paths)

# Turn interpretation into a graph object
G_I = nx.DiGraph()

for node, node_type in interpretation.species_assignments:
    G_I.add_node(node, type=node_type)

for (source, label), target in interpretation.attribute_paths:
    G_I.add_edge(source, target, label=label)

#The following constraint is equivalent to (: ~ noun)
target_sort = 'noun'
descriptions.get_entities_with_sort(G_I, 'noun')


#The following constraint is equivalent to (:PRD )
print(descriptions.get_sort(G_I, descriptions.traverse_path(G_I, 'u1', ['PRD'])))
print(descriptions.components(G_I, 'u2'))
