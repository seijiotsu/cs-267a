import abc

class Expr(abc.ABC):
    @abc.abstractmethod
    def accept(self, visitor, extra = None):
        raise NotImplementedError

class Entry(Expr):
    def __init__(self, sentence):
        self.sentence = sentence

    def accept(self, visitor, extra = None):
        return visitor.visitEntry(self, extra)

class Sentence(Expr):
    def __init__(self, orClause):
        self.orClause = orClause

    def accept(self, visitor, extra = None):
        return visitor.visitSentence(self, extra)

class OrClause(Expr):
    def __init__(self, andClauses):
        self.andClauses = andClauses

    def accept(self, visitor, extra = None):
        return visitor.visitOrClause(self, extra)

class AndClause(Expr):
    def __init__(self, clauses):
        self.clauses = clauses

    def accept(self, visitor, extra = None):
        return visitor.visitAndClause(self, extra)

class AtomClause(Expr):
    def __init__(self, atom):
        self.atom = atom

    def accept(self, visitor, extra = None):
        return visitor.visitAtomClause(self, extra)

class ExistsClause(Expr):
    def __init__(self, identifier, clause):
        self.identifier = identifier
        self.clause = clause
    
    def accept(self, visitor, extra = None):
        return visitor.visitExistsClause(self, extra)

class ForallClause(Expr):
    def __init__(self, identifier, clause):
        self.identifier = identifier
        self.clause = clause

    def accept(self, visitor, extra = None):
        return visitor.visitForallClause(self, extra)

class NotClause(Expr):
    def __init__(self, clause):
        self.clause = clause

    def accept(self, visitor, extra = None):
        return visitor.visitNotClause(self, extra)

class NestedSentence(Expr):
    def __init__(self, sentence):
        self.sentence = sentence

    def accept(self, visitor, extra = None):
        return visitor.visitNestedSentence(self, extra)

class Atom(Expr):
    def __init__(self, identifier, arguments):
        self.identifier = identifier
        self.arguments = arguments

    def accept(self, visitor, extra = None):
        return visitor.visitAtom(self, extra)

class StringArgument(Expr):
    def __init__(self, value):
        self.value = value

    def accept(self, visitor, extra = None):
        return visitor.visitStringArgument(self, extra)

class VariableArgument(Expr):
    def __init__(self, value):
        self.value = value

    def accept(self, visitor, extra = None):
        return visitor.visitVariableArgument(self, extra)