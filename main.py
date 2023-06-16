import cmd
from lang.QueryParser import parseQuery
from lang.LispifyVisitor import LispifyVisitor

from lifted_inference_utils import preprocess, is_independent, substitute
from db_utils import DatabaseConnection
import itertools
import math

def lift(cnf, db: DatabaseConnection, verbose = False):
    """
    The lifted inference algorithm.

    cnf:    the boolean formula in conjunctive normal form.
    P:      the probabilistic tuples we are evalulating.
    """

    if verbose:
        print('Lifting: ' + str(cnf))
    #
    # Step 0: Base of Recursion
    # In this step, we check whether or not the cnf is a single "ground atom" t.
    # What that means, I think, is that we are checking if the cnf is just for
    # example "Attends(John, UCLA)". If this is the case, we can just look it up
    # in the probabilistic database, and return the probability.
    #

    # check if format of query is (operator, instance). If that is the case it should exist in the database
    # TODO: handle base cases that are not in database
    if cnf[0] == 'atom' and cnf[2][0] == 'string' and cnf[1] in db.operators:
        # base case reached, query database
        return db.probability(cnf[1], cnf[2][1])
    # else check if we have a not followed by a operator keyword. If that is the case the negation should exist in the database
    elif cnf[0] == 'not':
        subcnf = cnf[1]
        if subcnf[0] == 'atom' and subcnf[2][0] == 'string' and subcnf[1] in db.operators:
            # base case reached, query database for the negation of the query
            return 1 - db.probability(subcnf[1], subcnf[2][1])
    # fault check
    if cnf[0] == 'atom' and cnf[2][0] == 'variable':
        raise Exception('Query is not grounded: ' + cnf)
    
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
    if verbose:
        print('Preprocessed: ' + str(cnf))

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
    # check that cnf is a ucnf (m > 1 covered in preprocess)
    if cnf[0] == 'or':
        m = len(cnf) - 1
        # check all ways to split cnf into two clauses:
        for i in range(1, math.floor(m/2) + 1):
            for set1 in itertools.combinations(cnf[1:], i):
                set2 = tuple(x for x in cnf[1:] if x not in set1)
                # turn sets into cnfs of ors
                if len(set1) == 1:
                    clause1 = set1[0]
                else:
                    clause1 = ['or', *set1]
                if len(set2) == 1:
                    clause2 = set2[0]
                else:
                    clause2 = ['or', *set2]
                if is_independent(clause1, clause2):
                    if verbose:
                        print('Independent: ' + str(clause1) + ' and ' + str(clause2))
                    return 1 - (1 - lift(clause1, db))*(1 - lift(clause2, db))
    # if program does not execute the return above, we continue

    #
    # Step 3: Inclusion-Exclusion
    #
    # If the clauses are not independent, that means we couldn't do the previous
    # step and we have to try another angle.
    # 
    # Inclusion-Exclusion, think venn diagrams.
    # cancellations is going to be a big part of this step, but first implementation will be without it.
    """code for step 3 here"""
    if cnf[0] == 'or':
        m = len(cnf) - 1
        returnval = 0
        # go through all areas of the venn diagram:
        # TODO: implement cancellations. If two subcnfs are the same, but are added with opposing signs, they cancel out.
        # proposed way to deal with cancellations: save all subcnfs. 
        # Then preprocess them in a way that makes them 'as simple as possible', so
        # that we can easily check if they are the same. 
        # Then we can check if they are the same, and if they are, we can remove them from the list if they have opposing signs.
        for i in range(1, m+1):
            for subset in itertools.combinations(cnf[1:], i):
                # turn subset tuple into cnf of ands
                subcnf = ['and', *subset]
                returnval += (-1)**(i+1) * lift(subcnf, db)
        return returnval


    #
    # Step 4: Decomposable Conjunction
    #
    # I think if our cnf has only a single clause, we skip steps 2 and 3 and
    # come straight here. So if we have Q1 ∧ Q2, we can just do:
    #   - p = L(Q1, P|Q1) * L(Q2, P|Q2)
    # and return that
    #
    if cnf[0] == 'and':
        m = len(cnf) - 1
        # check all ways to split cnf into two clauses:
        for i in range(1, math.floor(m/2) + 1):
            for set1 in itertools.combinations(cnf[1:], i):
                set2 = tuple(x for x in cnf[1:] if x not in set1)
                # turn sets into cnfs of ands
                if len(set1) == 1:
                    clause1 = set1[0]
                else:
                    clause1 = ['and', *set1]
                if len(set2) == 1:
                    clause2 = set2[0]
                else:
                    clause2 = ['and', *set2]
                if is_independent(clause1, clause2):
                    return lift(clause1, db) * lift(clause2, db)

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
    if cnf[0] == 'forall':
        returnval = 1
        variable = cnf[1]
        for instance in db.instances:
            subcnf = substitute(cnf[2], variable, instance)
            returnval *= lift(subcnf, db)
        return returnval

    if cnf[0] == 'exists':
        newquery = ['forall', cnf[1], ['not', cnf[2]]]
        return 1 - lift(newquery, db)

    #
    # Step 6: Fail
    #
    """code for step 6 here"""
    return -1 # fail

class QueryShell(cmd.Cmd):
    intro = 'Hello, this is the CS267A Probabilitic Database REPL. Type .help for help.\n'
    prompt = '>>> '

    help_msg = """
=== Help Menu ===

- Type '.quit' to quit.
- Type '.ops' for avaliable operators.
- Type '.instances' for avaliable instances.
- Type '.verbose' to toggle verbosity

- Type '.load X.db' to load file X.db
- Type '.load_default' to load the default 'main.db' database
    
Queries follow a format that mirrors First-Order logic:

    - Exists: '∃x' or '#x'
    - For all: '∀x' or '@x'
    - Atom: 'Name[x, y]'
    - And: '∧' or '&'
    - Or: '∨' or '|'
    - Not: '¬' or '~'
    
Quantifiers act like a unary operator in other languages, so use '()' to change its scope
For example:

#x (A[x] & B[x]) <-- can run this on .load_default
#x (Smoker[x] & ~Writer['Bob']) | @x1 @y1 @x2 @y2 (S[x1, y2] | R[y1] | S[x2, y2] | T[y2])

=== End Help ===
"""

    db = None

    is_verbose = False

    def onecmd(self, line):
        line = line.strip()
        if line == '.help':
            print(self.help_msg)
        elif line == '.quit':
            return True
        elif line == '.ops':
            if not self.db:
                print('You nee to load a database before you can access the available operators!')
            else:
                print(self.db.operators)
        elif line == '.instances':
            if not self.db:
                print('You nee to load a database before you can access the available instances!')
            else:
                print(self.db.instances)
        elif line == '.verbose':
            self.is_verbose = not self.is_verbose
            if self.is_verbose:
                print('Enabled verbose output')
            else:
                print('Disabled verbose output')
        elif line == '.load_default':
            self.db = DatabaseConnection('main.db')
        elif '.load' in line:
            line = line.split(' ')
            self.db = DatabaseConnection(line[1])
        else:
            try:
                parsedQuery = parseQuery(line)
                lispedQuery = LispifyVisitor().visitEntry(parsedQuery)
                res = lift(lispedQuery, self.db, self.is_verbose)
                print(res)
            except Exception as error:
                print(error)

if __name__ == '__main__':
    QueryShell().cmdloop()
