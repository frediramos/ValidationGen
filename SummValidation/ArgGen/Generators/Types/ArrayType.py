from pycparser.c_ast import *

import SummValidation.Utils.utils as utils
from ..ArrayGen import ArrayGen


#Create a symbolic N-dimension array
class ArrayTypeGen(ArrayGen):
    def __init__ (self, name, vartype, array, struct=False):
        super().__init__(name, vartype, array) 

        self.struct = struct


    #Array[i][j] = symbolic();
    def gen_array_init(self):
        name = self.argname.name

        index = f'{name}_idx_1'
        lvalue = ArrayRef(self.argname, subscript=ID(index))                                                              

        for i in range(2, self.dimension+1):
            
            index = f'{name}_idx_{i}'
            lvalue = ArrayRef(lvalue, subscript=ID(index))  
        
        if self.struct:
            rvalue = self.init_struct_rvalue(self.vartype)
        else:
            rvalue = self.symbolic_rvalue_array(Constant('string', f'\"{name}\"'), ID(index), self.vartype)
        
        return Assignment(op='=', lvalue=lvalue, rvalue=rvalue)             


    #Declare array and fill
    def gen(self):     
        code = []
        name = self.argname.name
        
        #Declare array
        code += self.gen_array_decl()
                                                            
        stmt = Compound([self.gen_array_init()])

        index = f'{name}_idx_{self.dimension}' 
        for_ast_code = self.For_ast(index, self._size(self.sizes[-1]), stmt)

        for i in range(self.dimension-2, -1 ,-1):
            index = f'{name}_idx_{i+1}'
            for_ast_code = self.For_ast(index, self._size(self.sizes[i]), Compound([for_ast_code])) 

        code.append(for_ast_code)

        #Terminate string with null byte ('\0')
        if self.vartype == 'char' and self.dimension == 1:
            size = self._size(self.sizes[-1])
            code.append(utils.terminate_string(self.argname, size))

        return code
