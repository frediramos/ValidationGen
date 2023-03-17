from pycparser.c_ast import *

from . Visitors.FunctionArgs import ArgVisitor

class Symbolic_Args():
    def __init__(self, args, size_macro = None, null_bytes = [],
                  max_macro = None, max_names = []):
       
        self.args = args

        if isinstance(size_macro, list):
            self.size_macro = size_macro.copy()
        else:
            self.size_macro = size_macro

        self.null_bytes = null_bytes
        self.max_macro = max_macro
        self.max_names = max_names
        
        if self.args == None:
            self.args = []

        self.block = []
        
        self.call_args = []
        self.types_list = []

        self.args_dict = {}

        #Visit arguments 
        for arg in self.args:
            
            size = self._get_val(self.size_macro)
            null = self._get_val(self.null_bytes)

            vis = ArgVisitor(size, null, self.max_macro, self.max_names)   
            vis.visit(arg)
            code = vis.gen_code()
            typ = vis.get_type()
            
            self.call_args.append(vis.argname)
            self.block += code
            self.types_list += typ
            
            self.args_dict[vis.argname] = typ

    def _get_val(self, arr):
        if isinstance(arr, list):
            if len(arr) > 1:
                return arr.pop(0)
            elif len(arr) == 1:
                return arr[0]
            else:
                return arr
        else:
            return arr

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