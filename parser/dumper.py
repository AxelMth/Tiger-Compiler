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
        # Always use parentheses to reflect grouping and associativity,
        # even if they may be superfluous.
        return "(%s %s %s)" % \
               (binop.left.accept(self), binop.op, binop.right.accept(self))

    @visitor(IfThenElse)
    def visit(self,ifThenElse):
        then_part,else_part = ifThenElse.then_part.accept(self),ifThenElse.else_part.accept(self)
        condition = ifThenElse.condition.accept(self)
        if else_part is not None:
            return "if %s then %s else %s" % (condition,then_part,else_part)
        else:
            return "if %s then %s" % (condition,then_part)

    @visitor(Identifier)
    def visit(self, id):
        if self.semantics:
            diff = id.depth - id.decl.depth
            scope_diff = "/*%d*/" % diff if diff else ''
        else:
            scope_diff = ''
        return '%s%s' % (id.name, scope_diff)

    @visitor(VarDecl)
    def visit(self,vardecl):
        dump_res = "var " + vardecl.name
        if vardecl.escapes and self.semantics:
            dump_res += "/*e*/"
        if vardecl.type is not None:
                dump_res += ": %s" % vardecl.type.typename
        dump_res += " := %s " % vardecl.exp.accept(self)
        return dump_res

    @visitor(FunDecl)
    def visit(self, fundecl):
        dump_res = "function " + fundecl.name + "("
        for arg in fundecl.args:
            dump_res += arg.name + ","
        dump_res += ") = %s " % fundecl.exp.accept(self)
        return dump_res

    @visitor(FunCall)
    def visit(self, funcall):
        dump_res = funcall.identifier.name + "("
        for param in funcall.params:
            dump_res += param.accept(self) + ","
        dump_res += ")"
        return dump_res

    @visitor(Let)
    def visit(self,let):
        dump_res = "let "
        for decl in let.decls:
            dump_res += "%s" % decl.accept(self)
        dump_res += "in "
        for exp in let.exps:
                dump_res += "%s" % exp.accept(self)
        return dump_res + " end"
