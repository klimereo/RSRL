import itertools

# The following two functions are used to traverse association sets
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


class rsrl_signatures:
    def check_partial_order(self, sorts, p_order):
        transitive = self.check_transitive(p_order)
        antisymmetric = self.check_antisymmetric(p_order)
        reflexive = self.check_reflexive(sorts, p_order)

        if not transitive:
            print("Error: Hierarchy is not transitive!")
        elif not antisymmetric:
            print("Error: Hierarchy is not antisymmetric!")
        elif not reflexive:
            print("Error: Hierarchy is not reflexive!")
        else:
            return True, print("Success: Hierarchy is a partial order.")

    def check_transitive(self, R):
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

    def check_antisymmetric(self, R):
        if not R:
            return True

        for a, b in R:
            if a != b and (b, a) in R:
                return False

        return True

    def check_reflexive(self, A, R):
        if A and not R:
            return False

        for a in A:
            if (a, a) not in R:
                return False

        return True

    def extract_maximal_reflexive(self, S, p_order):
        if self.check_partial_order(S, p_order):
            sorts = set()
            # Iterate through each tuple in the partial order
            for pair in p_order:
                # Check if the pair is reflexive and on the right side
                if pair[0] == pair[1]:
                    # Check if there is no other tuple with the same left side
                    if all(pair[0] != other_pair[0] for other_pair in p_order if pair != other_pair):
                        sorts.add(pair[0])
            return sorts

        else:
            print('Error: The type hierarchy is not a partial order!')

    def generate_paths(self, S, A):
        paths = set()
        for s1 in S:
            for s2 in S:
                for alpha in A:
                    paths.add((((s1, s2), alpha)))
        return paths

    def check_F(self, S, p_order, A, F):
        valid_features = []
        for s1 in S:
            for s2 in S:
                for alpha in A:
                    s1_tuple = (s1, alpha)
                    s2_tuple = (s2, alpha)
                    for input, output in F:
                        for order in p_order:
                            if s1_tuple == input and (s1, s2) == order:
                                s1_val = output
                                valid_features.append(((s1_tuple), s1_val))
                                for x, y in p_order:
                                    if x == s1_val:
                                        valid_features.append(((s2_tuple), y))
                                    else:
                                        continue
                            else:
                                continue

        if F == set(valid_features):
            print("Success: Appropriateness function is well-defined.")
            return True
        else:
            print("Error: Appropriateness function is ill-defined.")

    def check_rels(self, R, Ar):
        for element in R:
            if element not in Ar or not isinstance(Ar[element], int) or Ar[element] <= 0:
                return False, print('Error: Relations and their arities are ill-defined!')
        return True, print('Success: Relations and their arities are well-defined.')


class rsrl_descriptions:
    def generate_terms(self, V, A, max_len):
        # Here max len is needed as the definition of terms is infinitely recursive
        terms = []
        terms.append(":")
        for x in V:
            terms.append(x)
        for alpha in A:
            i = 0
            for tau in terms:
                terms.append(alpha + tau)
                i = i + 1
                if i == max_len + 1:
                    break
                else:
                    continue

        return terms

    def generate_formulae(self, S, T, R, Ar, V):
        formulae = []
        for sort in S:
            for term in T:
                formulae.append(f"{sort} ~ {term}")

        for term1 in T:
            for term2 in T:
                formulae.append(f"{term1} ≈ {term2}")

        for rel in R:
            arity = Ar[rel]
            var_string = list(V)[:arity]
            formulae.append(f"{rel}({var_string})")

        # Quantifiers and connectives lead to infinite recursion

        return formulae


class rsrl_interpretations:

    def is_valid_interpretation(self, signature, interpretation):
        A_sigma = signature[2]
        F_sigma = signature[3]
        Smax_sigma = signature[4]
        U = interpretation[0]
        Smax_ass = interpretation[1]
        A_int = interpretation[2]

        sort_assignment = self.check_sort_assignment(U, Smax_sigma, Smax_ass)
        attr_paths = self.check_attribute_paths(A_sigma, A_int, U, Smax_ass, F_sigma)

        if sort_assignment is not True:
            return False, print("Error: Interpretation is invalid. Sort assignment seems to be the issue.")
        elif attr_paths is not True:
            return False, print("Error: Interpretation is invalid. Attribute assignment seems to be the issue.")
        else:
            return True, print ("Success: Interpretation is valid.")

    def check_sort_assignment(self, U, S_max_sigma, Smax_ass):
        sorted_entities = []
        sorts_of_entities = []

        for entity, sort in Smax_ass:
            sorted_entities.append(entity)
            sorts_of_entities.append(sort)

        if (set(sorted_entities) == U) and (set(sorts_of_entities).issubset(S_max_sigma)):
            return True
        else:
            return False

    def check_attribute_paths(self, A_sigma, A_int, U, Smax_ass, F_sigma):
        # The presence of condition paths is to be checked in F_sigma
        tests = []
        for alpha in A_sigma:
            for u1 in U:
                if ((not(get_output_binary(u1, alpha, A_int)) or
                    get_output_binary(get_output_unary(u1, Smax_ass), alpha, F_sigma)) and
                        get_output_binary(get_output_unary(u1, Smax_ass), alpha, F_sigma) ==
                        get_output_unary(get_output_binary(u1, alpha, A_int), Smax_ass)):
                    tests.append(True)
                else:
                    tests.append(False)
                    continue

        for alpha in A_sigma:
            for u in U:
                if (not(get_output_binary(get_output_unary(u, Smax_ass), alpha, F_sigma)) or
                       get_output_binary(u, alpha, A_int)):
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