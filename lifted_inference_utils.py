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

    else: # basecase reached
        pass

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
        print(c1)
        print(c2)
        return True