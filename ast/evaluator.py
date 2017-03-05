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
        '''When BinaryOperator recognized, define how to behave.
        Return the result of the binary operation for each BinaryOperator.'''
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
        elif op == '<':
            return left < right
        elif op == '>':
            return left > right
        elif op == '=':
            return left == right
        elif op == '<=':
            return left <= right
        elif op == '>=':
            return left >= right
        elif op == '<>':
            return left != right
        else:
            raise SyntaxError("unknown operator %s" % op)

    @visitor(IfThenElse)
    def visit(self, ifThenElse):
        '''When IfThenElse recognized, define what to return.
        Return then_part if condition is true else return else_part.'''
        then_part = ifThenElse.then_part.accept(self)
        if ifThenElse.else_part is not None :
            else_part =  ifThenElse.else_part.accept(self)
        else:
            else_part = None
        condition = ifThenElse.condition.accept(self)
        if condition != 0:
            return then_part
        else:
            if else_part is not None:
                return else_part

    @visitor(None)
    def visit(self, node):
        raise SyntaxError("no evaluation defined for %s" % node)
