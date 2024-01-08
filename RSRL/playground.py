from rsrl import rsrl_sigma
from rsrl import rsrl_descs

rsrl_sigma = rsrl_sigma()
rsrl_descs = rsrl_descs()

S = {'top', 'sign', 'word', 'phrase', 'list'}
p_order = {('top', 'top'), ('sign', 'sign'), ('word', 'word'), ('phrase', 'phrase'), ('list', 'list'),
               ('top', 'sign'), ('top', 'list'),
               ('sign', 'word'), ('sign', 'phrase'), ('top', 'word'), ('top', 'phrase')}
A = {'DTRS', 'PHON', 'CASE'}
F = {(('sign', 'PHON'), 'list'),  (('word', 'PHON'), 'list'), (('phrase', 'PHON'), 'list'),
     (('word', 'CASE'), 'list'), (('phrase', 'DTRS'), 'list')}
S_max = rsrl_sigma.extract_maximal_reflexive(S, p_order)
R = {'member'}
Ar = {'member': 2}
valid_feats = rsrl_sigma.check_F(S, p_order, A, F)
rsrl_sigma.check_rels(R, Ar)


V = {"x", "y", "z", "q"}

possible_terms = rsrl_descs.generate_terms(V,A, max_len = 3)
possible_formulae = rsrl_descs.generate_formulae(S,possible_terms, R, Ar, V)
print(possible_formulae)
