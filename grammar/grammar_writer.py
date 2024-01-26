import json

# Specifying the signature
sorts = {'object', 'word', 'case', 'nom', 'acc', 'vform', 'boolean', 'verb', 'noun', '+', '-'}
hierarchy = {('object', 'object'), ('word', 'word'), ('case', 'case'), ('vform', 'vform'),
             ('boolean', 'boolean'), ('verb', 'verb'), ('noun', 'noun'), ('+', '+'), ('-', '-'),
             ('nom', 'nom'), ('acc', 'acc'), ('object', 'word'), ('object', 'verb'), ('object', 'noun'),
             ('object', 'case'), ('object', 'acc'),  ('object', 'nom'), ('object', 'vform'), ('object', 'boolean'),
             ('object', '+'), ('object', '-'), ('word', 'noun'), ('word', 'verb'),
             ('boolean', '+'), ('boolean', '-'), ('case', 'acc'), ('case', 'nom')}
attribute_symbols = {'PRD', 'VFORM', 'CASE'}
sort_attributes = {(('word', 'PRD'), 'boolean'),  (('verb', 'VFORM'), 'vform'),
                   (('verb', 'PRD'), '+'), (('noun', 'CASE'), 'case'), (('noun', 'PRD'), 'boolean')}
relation_symbols = {'member'}
arities = {'member': 2}

# Converting signature to dictionary format
signature = {
    'sorts': list(sorts),
    'hierarchy': [list(pair) for pair in hierarchy],
    'attribute_symbols': list(attribute_symbols),
    'sort_attributes': [([list(pair[0]), pair[1]]) for pair in sort_attributes],
    'relation_symbols': list(relation_symbols),
    'arities': arities
}

# Save to JSON file
with open('signature.json', 'w') as json_file:
    json.dump(signature, json_file, indent=2)

# Specifying an interpretation
universe = {"u1", "u2", "u3"}
species_assignments = {("u1", "noun"), ("u2", "nom"), ("u3", "+")}
attribute_paths = {(("u1", "CASE"), "u2"), (("u1", "PRD"), "u3")}


interpretation = {
    'universe': list(universe),
    'hierarchy': [list(pair) for pair in species_assignments],
    'attribute_paths': [([list(pair[0]), pair[1]]) for pair in attribute_paths]
}

# Save to JSON file
with open('interpretation.json', 'w') as json_file:
    json.dump(interpretation, json_file, indent=2)