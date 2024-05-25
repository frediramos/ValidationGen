from pycparser.c_ast import *

from SummValidation.APIGen.APIGen import API_Gen as API
from SummValidation.Utils.utils import returnValue

from . ArgGen import Symbolic_Args

class TestGen:
    def __init__(self, args, ret, cncrt_name, summ_name, memory, ret_memory, max_args):   
        self.args = args
        self.ret_type = ret
        self.memory = memory
        self.ret_memory = ret_memory
        self.cncrt_name = cncrt_name
        self.summ_name = summ_name
        self.max_args = max_args


    def tag_memory(self, ptr_names, size_macro):
        code = []
        if isinstance(size_macro, list):
            assert len(ptr_names) == len(size_macro)
            for ptr, size in zip(ptr_names, size_macro):
                code.append(API.mem_addr(ptr, size))
        else:
            for ptr in ptr_names:
                code.append(API.mem_addr(ptr, size_macro))
        return code


    def call_function(self, fname, call_args, ret_name, ret_type):
        lvalue = TypeDecl(ret_name, [], None, IdentifierType(names=[ret_type]))
        rvalue = FuncCall(ID(fname), ExprList([a for a in map(lambda x: ID(x), call_args)]))
        if ret_type =='void':
            return rvalue  
        return Decl(ret_name, [], [], [], [], lvalue, rvalue, None)

   
    def _run_function(self, fname:str, func_type:str,  ret_name:str, cnstr_name:str, id:int, args, size_macro):
        code = [self.call_function(fname, args, ret_name, self.ret_type)]

        if self.ret_memory:
            assert not isinstance(size_macro, list)
            code += [API.mem_addr(ret_name, size_macro, 'ret')]

        code += [
            API.get_cnstr(cnstr_name, ret_name, self.ret_type),
            API.store_cnstr(f'{func_type}_test{id}', cnstr_name),
        ]
        
        return code

    def run_concrete(self, id, args, size_macro):
        return self._run_function(self.cncrt_name, 'cnctr', 'ret1', 'cnstr1', id, args, size_macro)

    def run_summary(self, id, args, size_macro):
        return self._run_function(self.summ_name, 'summ', 'ret2', 'cnstr2', id, args, size_macro)


    def createTest(self, name, size_macro,
                    null_bytes, max_macro,
                      default, concrete, id):
        
        #Helper objects
        sym_args_gen = Symbolic_Args(self.args, size_macro, null_bytes, max_macro, self.max_args)

        #Create symbolic args
        args_code = sym_args_gen.create_symbolic_args(default, concrete)
        
        #Get ordered arg names
        args_name = sym_args_gen.get_all_args()

        #Body contains the test code
        body = [
            *args_code,
            API.save_current_state('initial_state'),
        ]

        if self.memory:
            ptr_names = sym_args_gen.get_ptr_args()
            body += self.tag_memory(ptr_names, size_macro)

        body += [
            *self.run_concrete(id, args_name, size_macro),
            
            API.halt_all('initial_state'),

            *self.run_summary(id, args_name, size_macro),

            API.halt_all('NULL'),

            API.check_implications('result', f'cnctr_test{id}', f'summ_test{id}'),
            API.print_counterexamples('result'),

            returnValue()
        ]

        #Create function ast
        block = Compound(body)
        
        typedecl = TypeDecl(name, [], None, IdentifierType(names=['void']))
        funcdecl = FuncDecl(None, typedecl)
        decl = Decl(name, [], [], [], [], funcdecl, None, None)
        
        return FuncDef(decl, None, block)

