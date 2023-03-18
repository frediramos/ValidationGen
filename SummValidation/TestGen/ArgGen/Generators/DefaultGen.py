from pycparser.c_ast import *

import SummValidation.Utils.utils as utils

class DefaultGen(NodeVisitor):
    def __init__ (self, name, vartype):

        #Size Macros
        self.sizeMacros = {
        'array':ID(utils.ARRAY_SIZE_MACRO),
        'ptr':ID(utils.POINTER_SIZE_MACRO)}

        self.argname = name #ID node
        self.vartype = vartype #String

        #Fuel Macro
        self.fuel = ID(utils.FUEL_MACRO)


    def init_struct_rvalue(self, vartype):
        vartype = self.vartype.replace(' ', '_')
        rvalue = FuncCall(ID(f'create_{vartype}'), ExprList([self.fuel]))
        return rvalue


    def type_size(self, vartype):
        return BinaryOp(op='*', left=FuncCall(ID('sizeof'),ExprList([ID(vartype)])), right=Constant('int', str(8)))

    def symbolic_rvalue(self, name):       
        sizeof = ExprList([name, self.type_size(self.vartype)])
        rvalue = FuncCall(ID('new_sym_var_named'), sizeof)
        return rvalue
    
    def const_rvalue(self, const):
        if isinstance(const, int):
            return Constant('int', str(const)) 
        elif isinstance(const, str):
            if len(const) == 1:
                return Constant('char', const)
            elif len(const) > 1:
                return Constant('string', const)
        
        return None