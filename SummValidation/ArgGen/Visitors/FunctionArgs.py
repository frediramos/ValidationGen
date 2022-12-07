from pycparser import parse_file, c_generator
from pycparser.c_ast import *

from ..Generators.Types.ArrayType import ArrayTypeGen
from ..Generators.Types.PrimitiveType import PrimitiveTypeGen
from ..Generators.Types.StructType import StructTypeGen

import SummValidation.Utils.utils as utils
from CProcessor import config



class ArgVisitor(NodeVisitor):

    def __init__ (self, sizeMacro = None, max_macro = None):

        #Store argument node (Decl)
        self.node = None

        # array or ptr
        if not sizeMacro:
            sizeMacro = 'ptr'
        
        self.sizeMacro = sizeMacro
        self.max_macro = max_macro

        #ID object
        self.argname = None 
        self.argtype = None

        #Array properties
        self.arrayDim = []

        #Struct properties
        self.struct = False

        #Final line(s) of code 
        self.code = []

    
    def get_type(self):
        return (self.argtype, self.arrayDim, self.struct)


    #Return generated code
    #If HEAP=true, change declaration of
    #arrays (dim: 2+) in function headers
    def gen_code(self):   
        return self.code

    #Visitors
    def visit(self, node):
        
        #Store top 'Decl' node
        if isinstance(node,Decl):
            self.node = node
        
        return NodeVisitor.visit(self, node)
    
    #Entry Node
    def visit_Decl(self, node):
        self.argname = node.name
        self.visit(node.type)                                                                    
        return

    #TypeDecl (Common node)
    def visit_TypeDecl(self, node):
        self.visit(node.type)
        argname = ID(self.argname)

        #Single
        if len(self.arrayDim) == 0:
            
            #Struct
            if self.struct:
                generator = StructTypeGen(argname, self.argtype)
                self.code = generator.gen()
                return
            
            #Primitive Type
            else:
                generator = PrimitiveTypeGen(argname, self.argtype, self.max_macro)
                self.code = generator.gen()
                return
        
        #Array or pointer
        else:
            if self.argtype == 'void':
                self.argtype = 'char'
            generator = ArrayTypeGen(argname, self.argtype, self.arrayDim, self.struct)
            self.code = generator.gen()
            return  
    

    #ArrayDecl
    def visit_ArrayDecl(self, node):
        if node.dim is not None:
            self.arrayDim.append(node.dim.value)

        else:
            self.arrayDim.append('array')

        self.visit(node.type)
        return


    #Pointer
    def visit_PtrDecl(self, node):
        if isinstance(node.type, FuncDecl):
            self.code = None
            return

        self.arrayDim.append(self.sizeMacro)
      
        self.visit(node.type)
        return

    
    #Struct Type
    def visit_Struct(self, node):
        self.argtype = f'struct {node.name}'
        self.struct = True
        return


    #IdentifierType (Common and last node)
    def visit_IdentifierType(self, node):
        typ = node.names[0]
        if len(node.names) > 1:
            for t in node.names[1:]:
                typ += f' {t}' 
        
        self.argtype = typ
        return

