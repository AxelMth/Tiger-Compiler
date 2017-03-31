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
            if vardecl.type.typename != "void":
                dump_res += ": %s" % vardecl.type.typename
        dump_res += " := %s " % vardecl.exp.accept(self)
        return dump_res

    @visitor(FunDecl)
    def visit(self, fundecl):
        dump_res = "function " + fundecl.name + "("
        if len(fundecl.args) == 1:
            dump_res += "%s: %s" % (fundecl.args[0].name, fundecl.args[0].type.typename)
        elif len(fundecl.args) > 1:
            for i in range(len(fundecl.args)-1):
                dump_res += "%s: %s," % (fundecl.args[i].name, fundecl.args[i].type.typename)
            dump_res += "%s: %s" % (fundecl.args[-1].name, fundecl.args[-1].type.typename)
        dump_res += ") "
        if fundecl.type is not None:
            if fundecl.type.typename != "void":
                dump_res += ": %s " % fundecl.type.typename
        dump_res += "= %s " % fundecl.exp.accept(self)
        return dump_res

    @visitor(FunCall)
    def visit(self, funcall):
        dump_res = funcall.identifier.name + "("
        if len(funcall.params) == 1:
            dump_res += "%s" % funcall.params[0].accept(self)
        elif len(funcall.params) > 1:
            for i in range(len(funcall.params)-1):
                dump_res += "%s," % funcall.params[i].accept(self)
            dump_res += "%s" % funcall.params[-1].accept(self)
        dump_res += ")"
        return dump_res

    @visitor(Let)
    def visit(self,let):
        dump_res = "let "
        for decl in let.decls:
            dump_res += "%s" % decl.accept(self)
        dump_res += "in "
        for i in range(len(let.exps)):
            if i != len(let.exps)-1:
                dump_res += "%s; " % let.exps[i].accept(self)
            else:
                dump_res += "%s" % let.exps[-1].accept(self)
        return dump_res + " end"

    @visitor(SeqExp)
    def visit(self,seq):
        dumb_res = ""
        if len(seq.exps) == 1:
            return seq.exps[0].accept(self)
        elif len(seq.exps) > 1:
            dumb_res = "("
            for i in range(len(seq.exps)-1):
                dumb_res += seq.exps[i].accept(self) + "; "
            dumb_res += seq.exps[-1].accept(self) + ")"
        else:
            dumb_res = "()"
        return dumb_res
