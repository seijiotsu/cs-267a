from Visitor import Visitor

class PrettyPrintVisitor(Visitor):
    def format(self, depth, name, *elements):
        padding = '  ' * (depth)
        formattedElements = []
        for elem in elements:
            if type(elem) is tuple:
                formattedElements.append(f'\n{padding}  {elem[0]}')
            else:
                formattedElements.append(f'\n{elem}')
        formatted = f'{padding}{name} [{"".join(formattedElements)} ]'
        return formatted

    def visitEntry(self, expr, extra = None):
        extra = { 'depth': 0 }
        output = self.format(extra['depth'], 'Entry', expr.sentence.accept(self, extra))
        return output
    
    def visitSentence(self, expr, extra = None):
        extra["depth"] += 1
        output = self.format(extra['depth'], 'Sentence', expr.orClause.accept(self, extra))
        extra["depth"] -= 1
        return output

    def visitOrClause(self, expr, extra = None):
        extra["depth"] += 1
        serializedAndClauses = [andClause.accept(self, extra) for andClause in expr.andClauses]
        output = self.format(extra['depth'], 'OrClause', *serializedAndClauses)
        extra["depth"] -= 1
        return output
    
    def visitAndClause(self, expr, extra = None):
        extra["depth"] += 1
        serializedClauses = [clause.accept(self, extra) for clause in expr.clauses]
        output = self.format(extra['depth'], 'AndClause', *serializedClauses)
        extra["depth"] -= 1
        return output
    
    def visitAtomClause(self, expr, extra = None):
        extra["depth"] += 1
        output = self.format(extra['depth'], 'AtomClause', expr.atom.accept(self, extra))
        extra["depth"] -= 1
        return output
    
    def visitExistsClause(self, expr, extra = None):
        extra["depth"] += 1
        output = self.format(extra['depth'], 'ExistsClause', (expr.identifier.value,), expr.clause.accept(self, extra))
        extra["depth"] -= 1
        return output
    
    def visitForallClause(self, expr, extra = None):
        extra["depth"] += 1
        output = self.format(extra['depth'], 'ForallClause', (expr.identifier.value,), expr.clause.accept(self, extra))
        extra["depth"] -= 1
        return output
    
    def visitNotClause(self, expr, extra = None):
        extra["depth"] += 1
        output = self.format(extra['depth'], 'NotClause', expr.clause.accept(self, extra))
        extra["depth"] -= 1
        return output
    
    def visitNestedSentence(self, expr, extra = None):
        extra["depth"] += 1
        output = self.format(extra['depth'], 'NestedSentence', expr.sentence.accept(self, extra))
        extra["depth"] -= 1
        return output
    
    def visitAtom(self, expr, extra = None):
        extra["depth"] += 1
        serializedArguments = [argument.accept(self, extra) for argument in expr.arguments]
        output = self.format(extra['depth'], 'Atom', (expr.identifier.value,), *[(a,) for a in serializedArguments])
        extra["depth"] -= 1
        return output
    
    def visitStringArgument(self, expr, extra = None):
        output = f'StringArgument [ "{expr.value}" ]'
        return output
    
    def visitVariableArgument(self, expr, extra = None):
        output = f'VariableArgument [ {expr.value} ]'
        return output