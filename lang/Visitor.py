import abc

class Visitor(abc.ABC):
    @abc.abstractmethod
    def visitEntry(self, expr, extra = None):
        raise NotImplementedError
    
    @abc.abstractmethod
    def visitSentence(self, expr, extra = None):
        raise NotImplementedError
    
    @abc.abstractmethod
    def visitOrClause(self, expr, extra = None):
        raise NotImplementedError
    
    @abc.abstractmethod
    def visitAndClause(self, expr, extra = None):
        raise NotImplementedError
    
    @abc.abstractmethod
    def visitAtomClause(self, expr, extra = None):
        raise NotImplementedError
    
    @abc.abstractmethod
    def visitExistsClause(self, expr, extra = None):
        raise NotImplementedError
    
    @abc.abstractmethod
    def visitForallClause(self, expr, extra = None):
        raise NotImplementedError
    
    @abc.abstractmethod
    def visitNotClause(self, expr, extra = None):
        raise NotImplementedError
    
    @abc.abstractmethod
    def visitNestedSentence(self, expr, extra = None):
        raise NotImplementedError
    
    @abc.abstractmethod
    def visitAtom(self, expr, extra = None):
        raise NotImplementedError
    
    @abc.abstractmethod
    def visitStringArgument(self, expr, extra = None):
        raise NotImplementedError
    
    @abc.abstractmethod
    def visitVariableArgument(self, expr, extra = None):
        raise NotImplementedError