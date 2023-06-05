from main import lift

# temporary database as a dictionary
db = {('A', 'a'): 0.1, ('A', 'b'): 0.2, ('A', 'c'): 0.3, ('A', 'd'): 0.4,
    ('B', 'a'): 0.5, ('B', 'b'): 0.6, ('B', 'c'): 0.7, ('B', 'd'): 0.8}

# test queries
queries = []
queries.append(['atom', 'A', ['string', 'a']]) # simple atom
# 0.1
queries.append(['not', ['atom', 'A', ['string', 'b']]]) # simple negation
# 0.8
queries.append(['and', ['atom', 'A', ['string', 'a']], ['atom', 'B', ['string', 'b']]]) # simple conjunction
# 0.1 * 0.6 = 0.06
queries.append(['or', ['atom', 'A', ['string', 'a']], ['atom', 'B', ['string', 'b']]]) # simple disjunction
# 1 - 0.9 * 0.4 = 0.64
queries.append(['forall', 'x', ['atom', 'A', ['variable', 'x']]]) # simple universal quantifier
# 0.1 * 0.2 * 0.3 * 0.4 = 0.0024
queries.append(['exists', 'x', ['atom', 'A', ['variable', 'x']]]) # simple existential quantifier
# 1 - 0.9 * 0.8 * 0.7 * 0.6 = 0.6976
queries.append(['forall', 'x', ['not', ['atom', 'A', ['variable', 'x']]]]) # simple universal negation
# 0.9 * 0.8 * 0.7 * 0.6 = 0.3024
queries.append(['not', ['exists', 'x', ['not', ['atom', 'A', ['variable', 'x']]]]]) # simple negated existential negation
# 1 - 0.3024 = 0.0.0024
queries.append(['and', ['not', ['exists', 'x', ['not', ['atom', 'A', ['variable', 'x']]]]], ['atom', 'B', ['string', 'd']]]) # simple conjunction of negated existential negation and atom
# 0.0024 * 0.8 = 0.00192
queries.append(['and', ['not', ['exists', 'x', ['not', ['atom', 'A', ['variable', 'x']]]]], ['or', ['atom', 'B', ['string', 'd']], ['atom', 'B', ['string', 'c']]]]) # simple conjunction of negated existential negation and disjunction
# 0.0024 * (1 - 0.2 * 0.3) = 0.0024 * 0.94 = 0.002256
queries.append(['exists', 'x', ['and', ['atom', 'A', ['variable', 'x']], ['atom', 'B', ['string', 'd']]]]) # simple existential quantifier
# (1 - 0.9*0.8*0.7*0.6) * 0.8 = 0.55808
queries.append(['exists', 'x', ['and', ['atom', 'A', ['variable', 'x']], ['atom', 'B', ['variable', 'x']]]]) # more advanced existential quantifier
# 0.5509008
queries.append(['forall', 'x', ['or', ['atom', 'A', ['variable', 'x']], ['atom', 'B', ['variable', 'x']]]]) # more advanced universal quantifier
# 0.2600048
queries.append(['forall', 'x', ['exists', 'y', ['and', ['atom', 'A', ['variable', 'x']], ['atom', 'B', ['variable', 'y']]]]]) # combination of quantifiers
# 0.0023712
queries.append(['forall', 'x', ['exists', 'y', ['or', ['atom', 'A', ['variable', 'x']], ['atom', 'B', ['variable', 'y']]]]]) # another combination of quantifiers
# 0.9644795551

corrects = [0.1, 0.8, 0.06, 0.64, 0.0024, 0.6976, 0.3024, 0.0024, 0.00192, 0.002256, 0.55808, 0.5509008, 0.2600048, 0.0023712, 0.9644795551]

answers = []
P = {'available_operators': ['A', 'B'], 'available_instances': ['a', 'b', 'c', 'd'], 'database': db}
for query in queries:
    print('testing:', query)
    res = lift(query, P)
    answers.append(res)
    print('returned:', res)
    print()

print('correct answers:', corrects)
print('answers:', answers)

hitrate = (1/len(answers)) * sum([1 if abs(answers[i] - corrects[i]) <= 1e-6 else 0 for i in range(len(answers))])
print('hitrate:', hitrate)