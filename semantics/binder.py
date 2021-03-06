from ast.nodes import *
from utils.visitor import *


class BindException(Exception):
    """Exception encountered during the binding phase."""
    pass


class Binder(Visitor):
    """The binder takes care of linking identifier uses to its declaration. If
    will also remember the depth of every declaration and every identifier,
    and mark a declaration as escaping if it is accessed from a greater depth
    than its definition.

    A new scope is pushed every time a let, function declaration or for loop is
    encountered. It is not allowed to have the same name present several
    times in the same scope.

    The depth is increased every time a function declaration is encountered,
    and restored afterwards.

    A loop node for break is pushed every time we start a for or while loop.
    Pushing None means that we are outside of break scope, which happens in the
    declarations part of a let."""

    def __init__(self):
        """Create a new binder with an initial scope for top-level
        declarations."""
        self.depth = 0
        self.scopes = []
        self.push_new_scope()
        self.add_intrinsics()
        self.break_stack = [None]

    def add_intrinsics(self):
        """Add intrinsics functions, which exist by default but do not
        need to be analyzed."""
        self.add_binding(FunDecl("print_int",
                                 [VarDecl("i", Type('int'), None)],
                                 Type('void'),
                                 Intrinsics()))
        self.add_binding(FunDecl("exit",
                                 [VarDecl("code", Type('int'), None)],
                                 Type('void'),
                                 Intrinsics()))
        # Push a new scope so that the intrinsics can be overriden if
        # needed.
        self.push_new_scope()

    def push_new_scope(self):
        """Push a new scope on the scopes stack."""
        self.scopes.append({})

    def pop_scope(self):
        """Pop a scope from the scopes stack."""
        del self.scopes[-1]

    def current_scope(self):
        """Return the current scope."""
        return self.scopes[-1]

    def push_new_loop(self, loop):
        """Push a new loop node on the break stack."""
        self.break_stack.append(loop)

    def pop_loop(self):
        """Pop a loop node from the break stack."""
        del self.break_stack[-1]

    def current_loop(self):
        loop = self.break_stack[-1]
        if loop is None:
            raise BindException("break called outside of loop")
        return loop

    def add_binding(self, decl):
        """Add a binding to the current scope and set the depth for
        this declaration. If the name already exists, an exception
        will be raised."""
        if decl.name in self.current_scope():
            raise BindException("name already defined in scope: %s" %
                                decl.name)
        self.current_scope()[decl.name] = decl
        decl.depth = self.depth

    def lookup(self, identifier):
        """Return the declaration associated with a identifier, looking
        into the closest scope first. If no declaration is found,
        raise an exception. If it is found, the decl and depth field
        for this identifier are set, and the escapes field of the
        declaration is updated if needed."""
        name = identifier.name
        for scope in reversed(self.scopes):
            if name in scope:
                decl = scope[name]
                identifier.decl = decl
                identifier.depth = self.depth
                decl.escapes |= self.depth > decl.depth
                return decl
        else:
            raise BindException("name not found: %s" % name)

    @visitor(Let)
    def visit(self,let):
        self.push_new_scope()
        self.push_new_loop(None)
        for decl in let.decls:
            decl.accept(self)
        self.pop_loop()
        for exp in let.exps:
            exp.accept(self)
        self.pop_scope()

    @visitor(VarDecl)
    def visit(self,var):
        var.exp.accept(self)
        self.add_binding(var)

    @visitor(FunDecl)
    def visit(self,fun):
        self.add_binding(fun)
        self.depth += 1
        self.push_new_scope()
        for arg in fun.args:
            self.add_binding(arg)
        fun.exp.accept(self)
        self.depth -= 1
        self.pop_scope()

    @visitor(FunCall)
    def visit(self,fun):
        fun_id = self.lookup(fun.identifier)
        if isinstance(fun_id,FunDecl):
            if len(fun_id.args) == len(fun.params):
                for param in fun.params:
                    param.accept(self)
            else:
                raise BindException("Wrong number of arguments while calling %s, expected %s, given %s" % (fun.identifier.name,len(fun_id.args),len(fun.params)))
        else:
            raise BindException("This id cannot be used as a function")

    @visitor(Identifier)
    def visit(self,ident):
        ident = self.lookup(ident)
        if isinstance(ident,FunDecl):
            raise BindException("A function cannot be used as a variable")

    @visitor(BinaryOperator)
    def visit(self,binop):
        binop.left.accept(self)
        binop.right.accept(self)

    @visitor(IfThenElse)
    def visit(self,ifthenelse):
        ifthenelse.condition.accept(self)
        ifthenelse.then_part.accept(self)
        if ifthenelse.else_part is not None:
            ifthenelse.else_part.accept(self)

    @visitor(IntegerLiteral)
    def visit(self,int):
        pass

    @visitor(SeqExp)
    def visit(self, seq):
        for exp in seq.exps:
            exp.accept(self)

    @visitor(Assignment)
    def visit(self,ass):
        previous_decl = self.lookup(ass.identifier)
        if not isinstance(previous_decl,VarDecl):
            raise BindException("Before assigning a variable, you should declare it !")
        ass.identifier.accept(self)
        ass.exp.accept(self)

    @visitor(While)
    def visit(self, whil):
        whil.condition.accept(self)
        self.push_new_loop(whil)
        whil.exp.accept(self)
        self.pop_loop()

    @visitor(For)
    def visit(self, fo):
        fo.low_bound.accept(self)
        fo.high_bound.accept(self)
        self.push_new_scope()
        self.add_binding(fo.indexdecl)
        self.push_new_loop(fo)
        fo.exp.accept(self)
        self.pop_loop()
        self.pop_scope()

    @visitor(Break)
    def visit(self, bra):
        bra.loop = self.current_loop()
        if not bra.loop:
            raise BindException("Break should be inside a loop")

    @visitor(None)
    def visit(self, node):
        raise BindException("Unable to bind %s" % node)
