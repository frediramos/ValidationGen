from pycparser.c_ast import *
from sympy import N

#Visit the ASt to separate each elemenet of interest
#function definitions; defined structs; and Typedefs 

class ReturnTypeVisior(NodeVisitor):
	def __init__ (self):
		self.name = None
		self.ptr = 0

	def get_ret(self):
		typ = self.name + self.ptr*'*'
		return typ

	def generic_visit(self, node):
		return node 

	def visit(self, node):
		if node is not None: 
			return NodeVisitor.visit(self, node)

	def visit_PtrDecl(self, node):
		self.ptr +=1
		self.visit(node.type)

	def visit_TypeDecl(self, node):
		self.visit(node.type)

	def visit_IdentifierType(self, node):
		self.name = node.names[0]


class InitialVisitor(NodeVisitor):

	def __init__ (self, ast, filename):

		self.file = filename
		self.ast = ast

		self._functions = {}
		self._function_args = {}

	def functions(self):
		if not self._functions:
			self.visit(self.ast)

		return self._functions
	
	def function_names(self):
		if not self._functions:
			self.visit(self.ast)
		
		return list(self._functions.keys())
	
	def function_args(self):
		if not self._function_args:
			self.visit(self.ast)
		
		return self._function_args

	def visit(self, node):
		if node is not None: 
			return NodeVisitor.visit(self, node)

	def visit_FuncDef(self, node):
		name = node.decl.name
		if name in self._functions.keys():
			sys.exit(f"ERROR: Mutiple functions with same name in: \'{self.file}\'") 

		self._functions[node.decl.name] = node
		self._function_args[node.decl.name] = node.decl.type.args.params if node.decl.type.args else None


class FCallsVisitor(NodeVisitor):

	def __init__ (self):
		self.calls = []

	def fcalls(self):
		return list(set(self.calls))

	def generic_visit(self, node):
		return node 

	def visit(self, node):
		if node is not None: 
			return NodeVisitor.visit(self, node)

	def visit_Assignment(self, node):
		self.visit(node.lvalue)
		self.visit(node.rvalue)

	def visit_Switch(self, node):
		self.visit(node.cond)
		self.visit(node.stmt)

	def visit_Return(self, node):
		self.visit(node.expr)

	def visit_Case(self, node):
		self.visit(node.expr)
		if node.stmts is not None:
			for stmt in node.stmts:
				self.visit(stmt)

	def visit_UnaryOp(self, node):
		self.visit(node.expr)

	def visit_BinaryOp(self, node):
		self.visit(node.left)
		self.visit(node.right)

	def visit_Compound(self, node):
		block = node.block_items
		if block is not None:
			for stmt in node.block_items:
				self.visit(stmt)
		return node

	def visit_Decl(self, node):
		self.visit(node.init)
		return node

	def visit_FuncDecl(self, node):
		args = node.args
		if args is not None:
			for decl in args.params:
				self.visit(decl)
		return node

	def visit_FuncDef(self, node):
		self.visit(node.decl.type)
		self.visit(node.body) 
		return node

	def visit_ExprList(self, node):
		exprs = node.exprs
		if exprs is not None:
			for expr in exprs:
				self.visit(expr)
		return node

	def visit_FuncCall(self, node):
		self.calls.append(node.name.name)
		self.visit(node.args)
		return node

	def visit_If(self, node):
		self.visit(node.cond)
		self.visit(node.iftrue)
		self.visit(node.iffalse)
		return node

	def visit_While(self, node):
		self.visit(node.stmt)
		return node

	def visit_For(self, node):
		self.visit(node.init)
		self.visit(node.stmt)
		self.visit(node.cond)
		return node
