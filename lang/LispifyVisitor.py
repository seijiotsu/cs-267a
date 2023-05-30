from Visitor import Visitor

class LispifyVisitor(Visitor):
    def visitEntry(self, expr, extra = None):
        return expr.sentence.accept(self)
    
    def visitSentence(self, expr, extra = None):
        return expr.orClause.accept(self)

    def visitOrClause(self, expr, extra = None):
        if len(expr.andClauses) == 1:
            return expr.andClauses[0].accept(self)
        return ['or', *[andClause.accept(self) for andClause in expr.andClauses]]
    
    def visitAndClause(self, expr, extra = None):
        if len(expr.clauses) == 1:
            return expr.clauses[0].accept(self)
        return ['and', *[clause.accept(self) for clause in expr.clauses]]
    
    def visitAtomClause(self, expr, extra = None):
        return expr.atom.accept(self)
    
    def visitExistsClause(self, expr, extra = None):
        return ['exists', expr.identifier.value, expr.clause.accept(self)]
    
    def visitForallClause(self, expr, extra = None):
        return ['forall', expr.identifier.value, expr.clause.accept(self)]
    
    def visitNotClause(self, expr, extra = None):
        return ['not', expr.clause.accept(self)]
    
    def visitNestedSentence(self, expr, extra = None):
        return expr.sentence.accept(self)

    def visitAtom(self, expr, extra = None):
        return [expr.identifier.value, *[arg.accept(self) for arg in expr.arguments]]
    
    def visitStringArgument(self, expr, extra = None):
        return ['string', expr.value]
    
    def visitVariableArgument(self, expr, extra = None):
        return ['variable', expr.value]
