from pycparser.c_ast import *

SIZE_MACRO = 'SIZE'
MAX_MACRO = 'MAX_NUM'
ARRAY_SIZE_MACRO = 'ARRAY_SIZE'
POINTER_SIZE_MACRO = 'POINTER_SIZE'


def defineMacro(label, value):
	return f'#define {label} {value}\n'

def defineInclude(name):
	return f'#include <{name}>\n'

def returnValue(val, operator=None):
	if operator:
		val = UnaryOp(operator, val)
	expr = ExprList([val])
	return Return(expr)


def createFunction(name, args, returnType):
	typedecl = TypeDecl(name, [], IdentifierType(names=[returnType]))
	funcdecl = FuncDecl(args, typedecl)
	decl = Decl(name, [], [], [], funcdecl, None, None)
	return decl


def mainFunction(calls):
	calls_ast = [c for c in map(lambda x : FuncCall(ID(x), ExprList([])), calls)]
	calls_ast.append(returnValue(Constant('int', str(0))))
	block = Compound(calls_ast)
	return block


def terminate_string(lvalue, size):
	arr_lvalue = ArrayRef(lvalue, subscript=size)
	assign = Assignment(op='=', lvalue=arr_lvalue, rvalue=Constant('char', '\'\\0\''))
	return assign   

