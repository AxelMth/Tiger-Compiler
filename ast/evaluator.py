from ast.nodes import *
from utils.visitor import visitor

class Evaluator:
    """This contains a simple evaluator visitor which computes the value
    of a tiger expression."""

    @visitor(IntegerLiteral)
    def visit(self, int):
        return int.intValue

    @visitor(BinaryOperator)
    def visit(self, binop):
        left, right = binop.left.accept(self), binop.right.accept(self)
        op = binop.op
        if op == '+':
            return left + right
        elif op == '*':
            return left * right
        elif op == '|':
            return left | right
        elif op == '&':
            return left & right
        elif op == '/':
            return left / right
        elif op == '-':
            return left - right
        else:
            raise SyntaxError("unknown operator %s" % op)

    @visitor(IfThenElse)
    def visit(self, ifThenElse):
        then_part, else_part = ifThenElse.then_part.accept(self), ifThenElse.else_part.accept(self)
        condition = ifThenElse.condition.accept(self)
        if condition != 0:
            return then_part
        else:
            return else_part

    @visitor(None)
    def visit(self, node):
        raise SyntaxError("no evaluation defined for %s" % node)
