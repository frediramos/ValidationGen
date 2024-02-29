from angr import SimProcedure
from collections import OrderedDict

from .constraints import RESTR_MAP
from .utils import *

from ..macros import SYM_VAR

#Symbolic variables generated
SYM_VARS = OrderedDict()


class new_sym_var(SimProcedure):

	def run(self, length):
		
		length = self.state.solver.eval(length)
		assert length % 8 == 0, "Size is in bits but must be divisible by 8!"
		
		sym_var = self.state.solver.BVS(SYM_VAR, length)		
		sym_var = sym_var.zero_extend(self.state.arch.bits - length)
		
		try:
			self.ret(sym_var)
		except Exception as e:
			print(e)


class new_sym_var_named(SimProcedure):

	def run(self, name_addr, length):
		
		length = self.state.solver.eval(length)
		assert length % 8 == 0, "Size is in bits but must be divisible by 8!"

		name = get_name(self.state, name_addr)
		assert(name not in SYM_VARS.keys())	
		
		sym_var = self.state.solver.BVS(name, length, explicit_name=True)
		SYM_VARS[name] = [sym_var]
			
		sym_var = sym_var.zero_extend(self.state.arch.bits - length)
		
		try:
			self.ret(sym_var)
		except Exception as e:
			print(e)


class new_sym_var_array(SimProcedure):

	def run(self, name_addr, index, length):
		
		length = self.state.solver.eval(length)
		assert length % 8 == 0, "Size is in bits but must be divisible by 8!"

		index = self.state.solver.eval(index)

		name = get_name(self.state, name_addr)
		bvname = f'{name}_{index}'
		
		sym_var = self.state.solver.BVS(bvname, length, explicit_name=True)

		if name not in SYM_VARS:
			SYM_VARS[name] = []
		
		SYM_VARS[name].append(sym_var)  

		sym_var = sym_var.zero_extend(self.state.arch.bits - length)

		try:
			self.ret(sym_var)
		except Exception as e:
			print(e)


class is_symbolic(SimProcedure):
	
	def run(self, var_addr, length):
		assert self.state.solver.eval(length) % 8 == 0,\
		 "Size is in bits but must be divisible by 8!"

		var = self.state.memory.load(var_addr, length/8, endness='Iend_LE')
		if self.state.solver.symbolic(var):
			self.ret(1)

		else:
			self.ret(0)


class maximize(SimProcedure):
	
	def run(self, sym_var_addr, length):
		sym_var = self.state.memory.load(sym_var_addr, length/8, endness='Iend_LE')
		constraints = tuple(self.state.solver.constraints)
		max_val = self.state.solver.max(sym_var, extra_constraints=(constraints))
		self.ret(max_val)


class minimize(SimProcedure):
	
	def run(self, sym_var_addr, length):
		sym_var = self.state.memory.load(sym_var_addr, length/8, endness='Iend_LE')
		constraints = tuple(self.state.solver.constraints)
		max_val = self.state.solver.min(sym_var, extra_constraints=(constraints))
		self.ret(max_val)


class is_sat(SimProcedure):
	def run(self, restr):
		restr_id = self.state.solver.eval(restr)
		restr = RESTR_MAP[restr_id]

		if self.state.solver.satisfiable(extra_constraints=(restr,)):
			self.ret(1)
		else:
			self.ret(0)


class assume(SimProcedure):
	def run(self, restr):
		restr_id = self.state.solver.eval(restr)
		restr = RESTR_MAP[restr_id]
		self.state.solver.add(restr)
		self.ret()
