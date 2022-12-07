from pycparser.c_ast import *
from .DefaultGen import DefaultGen



#Create a symbolic N-dimension array
class ArrayGen(DefaultGen):
    def __init__ (self, name, vartype, array):
        super().__init__(name, vartype) 

        self.sizes = array
        self.dimension = len(array)


    def _size(self, val):
        if val.isnumeric():
            return Constant('int', val)
        else:
            if val in self.sizeMacros.keys():
                return self.sizeMacros[val]
            else:
                return ID(val)


    #Declare N-dimension array in the stack
    #e.g array[10][5];
    def declare_stack_array(self):
        code = []
        name = self.argname.name
        
        typedecl = TypeDecl(name, [], IdentifierType(names=[self.vartype]))

        size = BinaryOp('+', self._size(self.sizes[-1]) , Constant('int', str(1)))
        array = ArrayDecl(typedecl, size, [])

        for i in range(self.dimension-2, -1, -1):
            array = ArrayDecl(array,  self._size(self.sizes[i]), [])

        code.append(Decl(name, [], [], [], array, None, None))
        return code  



    #Declare N-dimension array in the heap (uses malloc)
    #e.g *array = malloc(sizeof(int *) * 10);
    def declare_heap_array(self):

        code = []
        name = self.argname.name

        typedecl = TypeDecl(name, [], IdentifierType(names=[self.vartype]))

        #sizeof(int *)
        typtr = PtrDecl([], TypeDecl(name, [], IdentifierType([self.vartype])))
        for _ in range(1, self.dimension-1):
            typtr = PtrDecl([], typtr)
        sizeof = FuncCall(ID('sizeof'), ExprList([typtr]))
 
        #(sizeof(int *) * 10
        size = BinaryOp('*', sizeof, self._size(self.sizes[0]))

        #malloc(sizeof(int *) * 10);
        rvalue = FuncCall(ID('malloc'),ExprList([size]) )
        
        #int **array
        arrptr = PtrDecl([], typedecl)
        for _ in range(1, self.dimension):
            arrptr = PtrDecl([], arrptr)

        #int **array = malloc(sizeof(int) * 10);
        code.append(Decl(name, [], [], [], arrptr, rvalue, None))
        
        #For 2+ dimensions (e.g array[][])
        if self.dimension > 1:

            typtr = IdentifierType([self.vartype])
            sizeof = FuncCall(ID('sizeof'), ExprList([typtr]))
            
            index = f'malloc_idx_1'
            arrayref = ArrayRef(ID(name), ID(index))
            for i in range(2, self.dimension):
                index = f'malloc_idx_{i}'
                arrayref = ArrayRef(arrayref, ID(index))
            
            binop = BinaryOp('*', sizeof, self._size(self.sizes[-1]))
            stmt = Assignment('=', arrayref, FuncCall(ID('malloc'),ExprList([binop])))
            decls = self.For_ast(index, self._size(self.sizes[-2]), Compound([stmt]))

            typtr = PtrDecl([], TypeDecl(name, [], typtr))

            #For 3+ dimensions (e.g array[0][1][2])
            for i in range(self.dimension-2, 0,-1):

                index = f'malloc_idx_1'
                arrayref = ArrayRef(ID(name), ID(index))
                for j in range(2, i+1):
                    index = f'malloc_idx_{j}'
                    arrayref = ArrayRef(arrayref, ID(index))

                
                sizeof = FuncCall(ID('sizeof'), ExprList([typtr]))
                binop = BinaryOp('*', sizeof, self._size(self.sizes[i]))
                stmt = Assignment('=', arrayref, FuncCall(ID('malloc'),ExprList([binop])))
                decls = self.For_ast(index, self._size(self.sizes[i-1]), Compound([stmt,decls]))

                typtr = PtrDecl([], typtr)

            code.append(decls)

        return code



    def gen_array_decl(self):
        return self.declare_stack_array()


    #Standard 'for' loop to fill array
    def For_ast(self, index, size, stmt):

        ##For-init
        typedecl = TypeDecl(index, [], IdentifierType(names=['int']))
        decl = Decl(index, [], [], [], typedecl, Constant('int', str(0)), None)
        init  = DeclList(decls=[decl])
        
        ##For-condition
        cond = BinaryOp(op='<', left=ID(index), right=size)
        
        ##For-next
        nxt = UnaryOp(op='p++', expr=ID(index))

        ##Create the For node
        return For(init, cond, nxt, stmt)
        

    def symbolic_rvalue_array(self, name, index, vartype):
        
        #Multiply sizeof by 8bits
        multiply = BinaryOp(op='*', left=FuncCall(ID('sizeof'),ExprList([ID(vartype)])), right=Constant('int', str(8)))

        #Create Rvalue
        sizeof = ExprList([name, index, multiply])
        rvalue = FuncCall(ID('new_sym_var_array'), sizeof)

        return rvalue