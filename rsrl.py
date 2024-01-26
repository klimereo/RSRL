import itertools
import json

# Utility functions (to access outputs from sets of n-embedded ordered pairs given an input)
def get_output_unary(input_element, association_set):
    matching_tuple = next((tuple_element for tuple_element in association_set if input_element == tuple_element[0]),
                          None)
    if matching_tuple is not None:
        return matching_tuple[1]
    else:
        return None

def get_output_binary(input1, input2, association_set):
    matching_tuple = next(
        ((tuple_element[0][0], tuple_element[0][1], tuple_element[1]) for tuple_element in association_set if
         (input1, input2) == tuple_element[0]), None)

    if matching_tuple is not None:
        return matching_tuple[2]
    else:
        return None
        
# RSRL Signature is a 6-tuple
class Signatures:
    def __init__(self):
    	# Set of sort symbols
        self.sorts = set()
        # Partial order on sort symbols
        self.hierarchy = set()
        # Attribute symbols defined on sorts
        self.attribute_symbols = set()
        # Attribute appropriatenes function
        self.sort_attributes = set()
        # Maximally specific sorts --> species
        self.species = set()
        # Relation symbols
        self.relation_symbols = set()
        # Arities of relations
        self.arities = {}

    def add_sort(self, sort):
        self.sorts.add(sort)

    def add_partial_order_relation(self, s1, s2):
        self.hierarchy.add((s1, s2))

    def add_attribute_symbol(self, a):
        self.attribute_symbols.add(a)

    def add_sort_attribute(self, s1, a, s2):
        self.sort_attributes.add(((s1, a), s2))

    def add_relation_(self, rel):
        self.relation_symbols.add(rel)

    def add_arities(self, name, arity):
        self.arities[name] = arity

    def add_elements(self, sorts, hierarchy, attribute_symbols, sort_attributes, relation_symbols, arities):
        self.sorts.update(sorts)
        self.hierarchy.update(hierarchy)
        self.attribute_symbols.update(attribute_symbols)
        self.sort_attributes.update(sort_attributes)
        self.relation_symbols.update(relation_symbols)
        self.arities.update(arities)

    # The following function initiates a signature object, given an appropriately formatted .json file that corresponds to signature.
    def load_from_json(self, json_file_path):
        with open(json_file_path, 'r') as json_file:
            loaded_data = json.load(json_file)

        self.add_elements(
            set(loaded_data['sorts']),
            {(pair[0], pair[1]) for pair in loaded_data['hierarchy']},
            set(loaded_data['attribute_symbols']),
            {((pair[0][0], pair[0][1]), pair[1]) for pair in loaded_data['sort_attributes']},
            set(loaded_data['relation_symbols']),
            loaded_data['arities']
        )
        
    # The following functions check the RSRL well-formedness conditions on instantiated signature objects
    def is_partialorder(self, sorts, hierarchy):
        transitive = self.is_transitive(hierarchy)
        antisymmetric = self.is_antisymmetric(hierarchy)
        reflexive = self.is_reflexive(sorts, hierarchy)

        if not transitive:
            print("Error: Hierarchy is not transitive!")
        elif not antisymmetric:
            print("Error: Hierarchy is not antisymmetric!")
        elif not reflexive:
            print("Error: Hierarchy is not reflexive!")
        else:
            return True, print("Success: Hierarchy is a partial order.")

    @staticmethod
    def is_transitive(R):
        if not R:
            return True

        tup = {}
        for a, b in R:
            tup.setdefault(a, set()).add(b)

        for a, all_b_in_aRb in tup.items():
            for b in all_b_in_aRb:
                if b in tup and a != b:
                    all_c_in_bRc = tup[b]
                    if not all(c in all_b_in_aRb for c in all_c_in_bRc):
                        return False

        return True

    @staticmethod
    def is_antisymmetric(R):
        if not R:
            return True

        for a, b in R:
            if a != b and (b, a) in R:
                return False

        return True

    @staticmethod
    def is_reflexive(A, R):
        if A and not R:
            return False

        for a in A:
            if (a, a) not in R:
                return False

        return True

    @staticmethod
    def is_appropriate(sorts, hierarchy, attribute_symbols, sort_attributes):
        S = sorts
        A = attribute_symbols
        F = sort_attributes

        tests = []

        for s1 in S:
            for s2 in S:
                for alpha in A:
                    s1_tuple = (s1, alpha)
                    s2_tuple = (s2, alpha)
                    for x, y in F:
                        if ((not (get_output_binary(s1, alpha, F)) or ((s1, s2) in hierarchy)) and
                                 (get_output_binary(s2, alpha, F) and
                                 (get_output_binary(s1, alpha, F), get_output_binary(s2, alpha, F)) in hierarchy)):
                            tests.append(True)
                        else:
                            tests.append(False)

        if True in set(tests):
            return True, print("Success: Attribute appropriateness is well-defined.")
        elif False in set(tests):
            return False
        else:
            print("Attribute appropriateness check could not be verified for some reason.")



    @staticmethod
    def check_rels(R, Ar):
        for element in R:
            if element not in Ar or not isinstance(Ar[element], int) or Ar[element] <= 0:
                return False, print('Error: Relations and their arities are ill-defined!')
        return True, print('Success: Relations and their arities are well-defined.')
    
    def extract_species(self, sorts, hierarchy):
        if self.is_partialorder(sorts, hierarchy):
            species = set()
            # Iterate through each tuple in the partial order
            for pair in hierarchy:
                # Check if the pair is reflexive and on the right side
                if pair[0] == pair[1]:
                    # Check if there is no other tuple with the same left side
                    if all(pair[0] != other_pair[0] for other_pair in hierarchy if pair != other_pair):
                        species.add(pair[0])
            return species

        else:
            print('Error: The type hierarchy is not a partial order!')

# The current version does not implement relations in interpretations, i.e., I = <U,S,A>. 
class Interpretations:
    def __init__(self):
    	# The set of entities that populate the interpretation
        self.universe = set()
        # The set of sort assignments from entities to species
        self.species_assignments = set()
        # The set of labelled (with attributes) arcs
        self.attribute_paths = set()

    def add_entity(self, u):
        self.universe.add(u)

    def add_species_assignment(self, entity, species):
        self.universe.add((entity, species))

    def add_attribute_path(self, u1, attribute, u2):
        self.attribute_paths.add(((u1, attribute), u2))

    def add_elements(self, universe, species_assignments, attribute_paths):
        self.universe.update(universe)
        self.species_assignments.update(species_assignments)
        self.attribute_paths.update(attribute_paths)
	
    # The following function initiates an interpretation object, given an appropriately formatted .json file.
    def load_from_json(self, json_file_path):
        with open(json_file_path, 'r') as json_file:
            loaded_data = json.load(json_file)

        self.add_elements(
            set(loaded_data['universe']),
            {(pair[0], pair[1]) for pair in loaded_data['hierarchy']},
            {((pair[0][0], pair[0][1]), pair[1]) for pair in loaded_data['attribute_paths']}
        )

    def is_valid_interpretation(self,
                                attribute_symbols,
                                sort_attributes,
                                species,
                                universe,
                                species_assignments,
                                attribute_paths):

        sort_resolved = self.is_sortresolved(universe,
                                             species,
                                             species_assignments)

        well_typed = self.is_welltyped(attribute_symbols,
                                       attribute_paths,
                                       universe,
                                       species_assignments,
                                       sort_attributes)

        if sort_resolved is not True:
            return False, print("Error: Interpretation is invalid. Sort assignment seems to be the issue.")
        elif well_typed is not True:
            return False, print("Error: Interpretation is invalid. Attribute assignment seems to be the issue.")
        else:
            return True, print ("Success: Interpretation is valid.")

    @staticmethod
    def is_sortresolved(universe, species, species_assignments):
        sorted_entities = []
        sorts_of_entities = []

        # By comparing the sorts of entities with Smax, we essentially enforce sort-resolvedness
        for entity, sort in species_assignments:
            sorted_entities.append(entity)
            sorts_of_entities.append(sort)

        if (set(sorted_entities) == universe) and (set(sorts_of_entities).issubset(species)):
            return True
        else:
            return False

    @staticmethod
    def is_welltyped(attribute_symbols, attribute_paths, universe, species_assignments, sort_attributes):
        # The presence of condition paths is to be checked in sort_attributes
        tests = []
        for alpha in attribute_symbols:
            for u1 in universe:
                if ((not(get_output_binary(u1, alpha, attribute_paths)) or
                     get_output_binary(get_output_unary(u1, species_assignments), alpha, sort_attributes)) and
                        get_output_binary(get_output_unary(u1, species_assignments), alpha, sort_attributes) ==
                        get_output_unary(get_output_binary(u1, alpha, attribute_paths), species_assignments)):
                    tests.append(True)
                else:
                    tests.append(False)
                    continue

        for alpha in attribute_symbols:
            for u in universe:
                if (not(get_output_binary(get_output_unary(u, species_assignments), alpha, sort_attributes)) or
                       get_output_binary(u, alpha, attribute_paths)):
                    tests.append(True)
                else:
                    tests.append(False)
                    continue

        if True in set(tests):
            return True
        elif False in set(tests):
            return False
        else:
            print("Attribute assignment check could not be verified for some reason.")

class Descriptions:
    @staticmethod
    def get_sort(graph, node):
        if node in graph.nodes and 'type' in graph.nodes[node]:
            return graph.nodes[node]['type']
        else:
            print(f"Error: Node {node} does not have a 'type' attribute.")
            return None

    @staticmethod
    def get_entity_name(graph, node):
        if node in graph.nodes and 'name' in graph.nodes[node]:
            return graph.nodes[node]['name']
        else:
            print(f"Error: Node {node} does not have a 'name' attribute.")
            return None

    @staticmethod
    def get_entities_with_sort(graph, target_type):
        nodes_of_target_type = [node for node, data in graph.nodes(data=True) if data.get('type') == target_type]
        return nodes_of_target_type, print(f"':~{target_type}' denotes {nodes_of_target_type}")

    @staticmethod
    def traverse_path(graph, start_node, path):
        current_node = start_node

        for label in path:
            neighbors_with_label = [neighbor for neighbor, data in graph[current_node].items() if
                                    'label' in data and data['label'] == label]

            if not neighbors_with_label:
                print(f"No edge labeled '{label}' found from node {current_node}.")
                return None

            current_node = neighbors_with_label[0]

        return current_node

    @staticmethod
    def paths_are_equal(graph, path1, path2):
        for start_node in graph.nodes:
            path1_value = Descriptions.traverse_path(graph, start_node, path1)
            path2_value = Descriptions.traverse_path(graph, start_node, path2)


    @staticmethod
    def components(graph, start_node):
        visited = set()

        def dfs(current_node):
            visited.add(current_node)
            neighbors = graph.successors(current_node)  # For directed graph, use successors()

            for neighbor in neighbors:
                if neighbor not in visited:
                    dfs(neighbor)

        dfs(start_node)
        return visited

