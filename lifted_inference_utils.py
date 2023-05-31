# query formats:
# - ['not', query]
# - ['and', query1, query2, ...]
# - ['or', query1, query2, ...]
# - ['forall', variable, query]
# - ['exists', variable, query]
# - ['atom', predicate, ['string'/'variable', str/x]]

def preprocess_iteration(query):
    """
    Preprocessing the given query into a simpler one
    Operations that are made:

    starting with 'not':
    - removing double negation
    - moving nots 'inwards' of forall: ['not', ['forall', x, q]] => ['exists', x, ['not', q]]
    - moving nots 'inwards' of exists: ['not', ['exists', x, q]] => ['forall', x, ['not', q]]
    - moving nots 'inwards' of ands. ['not', ['and', q1, q2]] => ['and', ['not', q1], ['not', q2]]

    starting with 'and':
    - simplifying nestled ands: ['and', ['and',q1,q2], q3] => ['and', q1, q2, q3]
    - bringing out ors of ands to create ucnf: ['and', ['or',q1,q2], q3] => ['or', ['and', q1, q3], ['and', q2, q3]]
    - preprocess all subqueries q: ['and', q]

    starting with 'or':
    - simplifying nestled ors: ['or', ['or',q1,q2], q3] => ['or', q1, q2, q3]
    - preprocess all subqueries q: ['or', q]

    starting with 'forall':
    - distributing the forall into ands: ['forall', x, ['and', q1, q2]] => ['and', ['forall', x, q1], ['forall', x, q2]]
    (may not be necessary, not yet implemented)
    - preprocess all subqueries q: ['and', q]

    starting with 'exists':
    - distributing the exists into ors: ['exists', x, ['or', q1, q2]] => ['or', ['exists', x, q1], ['exists', x, q2]]
    (may not be necessary, not yet implemented)
    - preprocess all subqueries q: ['and', q]

    query:  query, not necessarily in cnf form
    """
    passed = True
    # operations to be done if first keyword is 'not'
    if query[0] == 'not':
        # removing double negation
        if query[1][0] == 'not':
            passed = False
            new_query = query[1][1]

        # moving nots 'inwards' of forall
        elif query[1][0] == 'forall':
            passed = False
            variable = query[1][1]
            subquery = query[1][2]
            new_query = ['exists', variable, ['not', subquery]]

        # moving nots 'inwards' of exists
        elif query[1][0] == 'exists':
            passed = False
            variable = query[1][1]
            subquery = query[1][2]
            new_query = ['forall', variable, ['not', subquery]]

        # moving nots 'inwards' of ands
        elif query[1][0] == 'and':
            passed = False
            subqueries = query[1][1:]
            new_query = ['or']
            for i in range(len(subqueries)):
                new_query.append(['not', subqueries[i]])

        # moving nots 'inwards' of ors
        elif query[1][0] == 'or':
            passed = False
            subqueries = query[1][1:]
            new_query = ['and']
            for i in range(len(subqueries)):
                new_query.append(['not', subqueries[i]])

    # operations to be done if first keyword is 'and'
    elif query[0] == 'and':
        # if there is only one argument, return that argument
        if len(query) == 2:
            passed = False
            new_query = query[1]

        # if there are more than one argument, we loop over arguments to simplify
        for arg in range(1, len(query)): # looping over all possible arguments
            # simplifying nestled ands
            if query[arg][0] == 'and':
                passed = False
                subqueries = query[arg][1:]
                query.pop(arg)
                new_query = query + subqueries
                break

            # bringing out ors of ands to create ucnf
            elif query[arg][0] == 'or':
                passed = False
                subqueries = query[arg][1:]
                query.pop(arg)
                residuals = query[1:]
                new_query = ['or']
                for i in range(len(subqueries)):
                    new_query.append(['and', subqueries[i]] + residuals)
                break
            
            # preprocess subquery 
            else:
                query[arg] = preprocess(query[arg])

    # operations to be done if first keyword is 'or'
    elif query[0] == 'or':
        # if there is only one argument, return that argument
        if len(query) == 2:
            passed = False
            new_query = query[1]

        # if there are more than one argument, we loop over arguments to simplify
        for arg in range(1, len(query)): # looping over all possible arguments
            # simplifying nestled ors
            if query[arg][0] == 'or':
                passed = False
                subqueries = query[arg][1:]
                query.pop(arg)
                new_query = query + subqueries
                break
            
            # preprocess subquery
            else:
                query[arg] = preprocess(query[arg])

    # operations to be done if first keyword is 'forall'
    elif query[0] == 'forall':
        # temp
        if False:
            pass

        # preprocess subquery
        else:
            query[2] = preprocess(query[2])

    # operations to be done if first keyword is 'exists'
    elif query[0] == 'exists':
        # temp
        if False:
            pass

        # preprocess subquery
        else:
            query[2] = preprocess(query[2])

    # operations to be done if first keyword is 'atom'
    elif query[0] == 'atom':
        # check if atom contains a variable, this shouldnt happen so we throw error
        if query[2][0] == 'variable':
            raise Exception('Atom contains variable: ' + query[2][1])

    else: # error
        raise Exception('Invalid keyword: ' + query[0])

    # check if no change was made to query
    if passed:
        new_query = query
    return new_query, passed

def preprocess(query):
    while True:
        query, passed = preprocess_iteration(query)
        if passed:
            break
    return query

def is_independent(c1, c2):
        # check if partition is independent
        # for now we assume that each predicate in the database is independent of every other predicate, which makes 
        # the partition independent no predicates are shared between the partitions
        # however, queries can be independent even if they share predicates, as long as they are grounded differently
        # cx_predicates is a list of tuples, where each tuple is a predicate and its grounded variable. If not grounded, the variable is None
        c1_predicates = get_predicates(c1)
        c2_predicates = get_predicates(c2)
        return disjunct_sets(c1_predicates, c2_predicates)

def disjunct_sets(set1, set2):
    # returns true if the sets are disjunct, false otherwise
    set2_predicates = [tup[0] for tup in set2]
    for tup in set1:
        predicate = tup[0]
        if tup[1] == None: # if predicate is not grounded, sets are not disjunct if predicate is in set2
            if predicate in set2_predicates:
                return False
        else:
            if tup in set2: # if predicate is grounded, sets are not disjunct if predicate is in set2 with same ground.
                return False
    return True

def get_predicates(query):
    # returns a list of tuples, where each tuple is a predicate and its grounded variable. If not grounded, the variable is None
    predicates = []
    if query[0] == 'atom' and query[2][0] == 'variable':
        predicates.append((query[1], None))
    elif query[0] == 'atom' and query[2][0] == 'string':
        predicates.append((query[1], query[2][1]))
    elif query[0] == 'and' or query[0] == 'or':
        for subquery in query[1:]:
            predicates += get_predicates(subquery)
    elif query[0] == 'not':
        predicates += get_predicates(query[1])
    elif query[0] == 'forall' or query[0] == 'exists':
        predicates += get_predicates(query[2])
    else:
        raise Exception('Invalid keyword: ' + query[0])
    
def substitute(query, var, instance):
    # substitutes all instances of var in query with instance
    if query[0] == 'atom' and query[2][0] == 'variable' and query[2][1] == var:
        query[2] = ['string', instance]
    elif query[0] == 'and' or query[0] == 'or':
        for i, subquery in enumerate(query[1:]):
            query[i] = substitute(subquery, var, instance)
    elif query[0] == 'not':
        query[1] = substitute(query[1], var, instance)
    else:
        raise Exception('Invalid keyword: ' + query[0])
    return query

