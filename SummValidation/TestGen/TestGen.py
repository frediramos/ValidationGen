from pycparser.c_ast import *

from SummValidation.APIGen.APIGen import API_Gen
from SummValidation.Utils.utils import returnValue

from . ArgGen import Symbolic_Args

class TestGen:
    def __init__(self, args, ret, cncrt_name, summ_name, memory):   
        self.args = args
        self.ret = ret
        self.memory = memory
        self.cncrt_name = cncrt_name
        self.summ_name = summ_name


    def call_function(self, fname, call_args, ret_name, ret_type):
        lvalue = TypeDecl(ret_name, [], IdentifierType(names=[ret_type]))
        rvalue = FuncCall(ID(fname), ExprList([a for a in map(lambda x: ID(x), call_args)]))
        if ret_type =='void':
            return rvalue  
        return Decl(ret_name, [], [], [], lvalue, rvalue, None)


    def createTest(self, name, size_macro, max_macro, id):

        #Helper objects
        sym_args_gen = Symbolic_Args(self.args, size_macro, max_macro)
        api_gen = API_Gen()

        #Create symbolic args
        args_code = sym_args_gen.create_symbolic_args()
        
        #Get ordered arg names
        args_names = sym_args_gen.get_all_args()

        #Body contains the test code
        body = [
            *args_code,
            api_gen.save_current_state('initial_state'),
        ]

        if self.memory:
            ptr_names = sym_args_gen.get_ptr_args()
            for ptr in ptr_names:
                body.append(api_gen.mem_addr(ptr, size_macro))

        body +=[
            self.call_function(self.cncrt_name, args_names, 'ret1', self.ret),
            api_gen.get_cnstr('cnstr1', 'ret1', self.ret),
            api_gen.store_cnstr(f'cnctr_test{id}', 'cnstr1'),
            
            api_gen.halt_all('initial_state'),

            self.call_function(self.summ_name, args_names, 'ret2', self.ret),			
            api_gen.get_cnstr('cnstr2', 'ret2', self.ret),
            api_gen.store_cnstr(f'summ_test{id}', 'cnstr2'),

            api_gen.halt_all('NULL'),

            api_gen.check_implications('result', f'cnctr_test{id}', f'summ_test{id}'),
            api_gen.print_counterexamples('result'),

            #Return
            returnValue(None)
        ]

        #Create function ast
        block = Compound(body)
        
        typedecl = TypeDecl(name, [], IdentifierType(names=['void']))
        funcdecl = FuncDecl(None, typedecl)
        decl = Decl(name, [], [], [], funcdecl, None, None)
        
        
        return FuncDef(decl, None, block)

