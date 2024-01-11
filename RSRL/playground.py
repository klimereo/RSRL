import random

from rsrl import rsrl_signatures
from rsrl import rsrl_descriptions
from rsrl import rsrl_interpretations

rsrl_s = rsrl_signatures()
rsrl_d = rsrl_descriptions()
rsrl_i = rsrl_interpretations()

# Defining the signature (ontology)

S_sigma = {'top', 'sign', 'word', 'phrase', 'list'}
p_order = {('top', 'top'), ('sign', 'sign'), ('word', 'word'), ('phrase', 'phrase'), ('list', 'list'),
               ('top', 'sign'), ('top', 'list'),
               ('sign', 'word'), ('sign', 'phrase'), ('top', 'word'), ('top', 'phrase')}
A_sigma = {'DTRS', 'PHON', 'CASE'}
F_sigma = {(('sign', 'PHON'), 'list'),  (('word', 'PHON'), 'list'), (('phrase', 'PHON'), 'list'),
     (('word', 'CASE'), 'list'), (('phrase', 'DTRS'), 'list')}
S_max_sigma = rsrl_s.extract_maximal_reflexive(S_sigma, p_order)
R_sigma = {'member'}
Ar_sigma = {'member': 2}
valid_feats = rsrl_s.check_F(S_sigma, p_order, A_sigma, F_sigma)
rsrl_s.check_rels(R_sigma, Ar_sigma)
Vars = {"x", "y", "z", "q"}

SIGNATURE = (S_sigma, p_order, A_sigma, F_sigma, S_max_sigma, R_sigma, Ar_sigma, Vars)

# Checking description syntax

possible_terms = rsrl_d.generate_terms(Vars,A_sigma, max_len = 3)
print("Some well-formed terms:", random.choices(possible_terms, k=6))
possible_formulae = rsrl_d.generate_formulae(S_sigma,possible_terms, R_sigma, Ar_sigma, Vars)
print("Some well-formed formulae:", random.choices(possible_formulae, k=16))


# Specifying an interpretation
U_int = {"u1", "u2", "u3"}
Smax_ass = {("u1", "word"), ("u2", "list"), ("u3", "list")}
A_int = {(("u1", "PHON"), "u2"), (("u1", "CASE"), "u3")}

INTERPRETATION = (U_int, Smax_ass, A_int)

rsrl_i.is_valid_interpretation(SIGNATURE, INTERPRETATION)
