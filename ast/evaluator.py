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
        op = binop.op
        if op == '&':
            left = binop.left.accept(self)
            if left == 0:
                return 0
            right = binop.right.accept(self)
            if right == 0:
                return 0
            else:
                return 1
        left,right = binop.left.accept(self),binop.right.accept(self)
        if op == '+':
            return left + right
        elif op == '*':
            return left * right
        elif op == '|':
            if left != 0 or right != 0:
                return 1
            return 0
        elif op == '/':
            return left // right
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

    @visitor(SeqExp)
    def visit(self,seq):
        for i in range(len(seq.exps)-1):
            seq.exps[i].accept(self)
        return seq.exps[-1].accept(self)

    @visitor(None)
    def visit(self, node):
        raise SyntaxError("no evaluation defined for %s" % node)
