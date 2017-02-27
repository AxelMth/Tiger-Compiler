from ast.nodes import *
from utils.visitor import *

class Dumper(Visitor):

    def __init__(self, semantics):
        """Initialize a new Dumper visitor. If semantics is True,
        additional information will be printed along with declarations
        and identifiers."""
        self.semantics = semantics

    @visitor(None)
    def visit(self, node):
        raise Exception("unable to dump %s" % node)

    @visitor(IntegerLiteral)
    def visit(self, i):
        return str(i.intValue)

    @visitor(BinaryOperator)
    def visit(self, binop):
        # Always use parentheses to reflect grouping and associativity, even if they may
        # be superfluous.
        return "(%s %s %s)" % (binop.left.accept(self), binop.op, binop.right.accept(self))
    

    @visitor(IfThenElse)
    def visit(self,ifThenElse):
        then_part,else_part = ifThenElse.then_part.accept(self),ifThenElse.else_part.accept(self)
        condition = ifThenElse.condition.accept(self)
        return "if %s then %s else %s" % (condition,then_part,else_part)
    
    @visitor(Identifier)
    def visit(self, id):
        return id.name
