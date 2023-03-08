from pycparser.c_ast import *

from . Visitors.FunctionArgs import ArgVisitor

class Symbolic_Args():
    def __init__(self, args, size_macro = None, max_macro = None):
        self.args = args
        self.size_macro = size_macro
        self.max_macro = max_macro
        
        if self.args == None:
            self.args = []

        self.block = []
        
        self.call_args = []
        self.types_list = []

        self.args_dict = {}

        #Visit arguments 
        for arg in self.args:

            vis = ArgVisitor(self.size_macro, self.max_macro)   
            vis.visit(arg)
            code = vis.gen_code()
            typ = vis.get_type()
            
            self.call_args.append(vis.argname)
            self.block += code
            self.types_list += typ
            
            self.args_dict[vis.argname] = typ


    def create_symbolic_args(self):
        return self.block

    def get_types(self):  
        return self.types_list

    def get_all_args(self):
        return self.call_args

    def get_ptr_args(self):
        ptr_names = []
        for name in self.args_dict.keys():
            if len(self.args_dict[name][1]) > 0:
                ptr_names.append(name)
        
        return ptr_names   