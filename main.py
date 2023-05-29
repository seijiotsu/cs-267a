from lifted_inference_utils import preprocess, is_independent

def lift(cnf, P):
    """
    The lifted inference algorithm.

    cnf:    the boolean formula in conjunctive normal form.
    P:      the probabilistic tuples we are evalulating.
    """

    #
    # Step 0: Base of Recursion
    # In this step, we check whether or not the cnf is a single "ground atom" t.
    # What that means, I think, is that we are checking if the cnf is just for
    # example "Attends(John, UCLA)". If this is the case, we can just look it up
    # in the probabilistic database, and return the probability.
    #

    # check if formot of query is (operator, instance). If that is the case it should exist in the database
    if cnf[0] in P['available_operators'] and cnf[1] in P['available_instances']:
        # base case reached, query database
        return 1
    # else check if we have a not followed by a operator keyword. If that is the case the negation should exist in the database
    # TODO
    # else not base case reached, keep going


    #
    # Step 1: Rewriting of Query
    # If the cnf is not a single ground atom, that means we might have something
    # like
    #       ∀x ∀y ∀z ∀w  (S(x,y) ∨ R(y) ∨ S(z,w) ∨ T(w))
    #
    # we can rewrite this by separating out the atoms based on their common
    # variables. So in this case, we can separate it into:
    #
    #       (∀x ∀y S(x,y) ∨ R(y)) ∨ (∀z ∀w S(z,w) ∨ T(w))
    #
    # so I think this step is about separating out the variables?
    #

    cnf = preprocess(cnf)

    #
    # Step 2: Decomposable disjunction
    #
    # If we have (∀x ∀y S(x,y) ∨ R(y)) ∨ (∀z ∀w S(z,w) ∨ T(w)) then we see that
    # the two clauses are independent:
    #   - Q1 = (∀x ∀y S(x,y) ∨ R(y))
    #   - Q2 = (∀z ∀w S(z,w) ∨ T(w))
    #
    # so we can simply evaluate them separately.
    #
    # and then simply evaluate the following:
    #   - p1 = lift(Q1, P|Q1)
    #   - p2 = lift(Q2, P|Q2)
    #   - p  = 1 - (1 - p1)*(1 - p2)
    #   and voila
    #
    """code for step 2 here"""
    # check that cnf is a ucnf with m > 1
    print(cnf)
    if cnf[0] == 'or':
        m = len(cnf) - 1
        # check all partitions of cnf for independence
        for i in range(1, m):
            for partition in itertools.combinations(cnf[1:], i):
                # check if partition is independent
                if is_independent(partition):
                    # partition is independent, evaluate
                    pass
                
    #
    # Step 3: Inclusion-Exclusion
    #
    # If the clauses are not independent, that means we couldn't do the previous
    # step and we have to try another angle.
    #
    # There's some complex formula here that I don't really understand
    #
    """code for step 3 here"""

    #
    # Step 4: Decomposable Conjunction
    #
    # I think if our cnf has only a single clause, we skip steps 2 and 3 and
    # come straight here. So if we have Q1 ∧ Q2, we can just do:
    #   - p = L(Q1, P|Q1) * L(Q2, P|Q2)
    # and return that
    #
    """code for step 4 here"""

    #
    # Step 5: Decomposable Universal Quantifier
    # 
    # I think what this step is saying is, if we have like Student(x, UCLA)
    # then we can do something like this:
    #
    #   p = 0
    #   for person in x:
    #       p += L(Q[x/person], P|x=person)
    #
    """code for step 5 here"""

    #
    # Step 6: Fail
    #
    """code for step 6 here"""

#cnf = ("happy", "John")
P = {'available_operators': ["q", "q2", "q3"], 'available_instances': ["John"]}

test = ['and', ['not', ['exists', 'x', ['not', 'q']]], ['or', 'q2', 'q3']]
#test = ['and', 'q', ['and', 'q2', 'q3']]

print(test)
simplified = preprocess(test)
print(simplified)
lift(simplified,P)