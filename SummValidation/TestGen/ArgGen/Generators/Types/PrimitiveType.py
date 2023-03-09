from pycparser.c_ast import *
from ..DefaultGen import DefaultGen


# Create a primitive symbolic var

class PrimitiveTypeGen(DefaultGen):
    def __init__ (self, name, vartype, max_macro = None):
        super().__init__(name, vartype)

        self.max_macro = max_macro


    #size_t max = MAX_NUM_1;
    #assume(_solver_LE(&n, &max, sizeof(size_t) * 8));
    
    def _limit_max(self, name):

        lvalue = TypeDecl('max', [], IdentifierType(names=[self.vartype]))
        rvalue = ID(self.max_macro)
        decl = Decl('max', [], [], [], lvalue, rvalue, None)

        max = UnaryOp('&', ID('max'))
        value = UnaryOp('&', ID(name))
        size = self.type_size(self.vartype)

        le = FuncCall(ID('_solver_LE'), ExprList([value, max, size]))
        assume = FuncCall(ID('assume'), ExprList([le]))

        return[decl, assume]


    # e.g, int a = summ_new_sym_var(sizeof(int))   
    def gen(self):

        code = []
        name = self.argname.name

        #Declare Variable
        lvalue = TypeDecl(name, [], IdentifierType(names=[self.vartype]))

        #Make symbolic type
        rvalue = self.symbolic_rvalue(Constant('string', f'\"{name}\"'))

        #Assemble declaration
        decl = Decl(name, [], [], [], lvalue, rvalue, None)
        code.append(decl)

        if self.max_macro:
            code += self._limit_max(name)
        return code