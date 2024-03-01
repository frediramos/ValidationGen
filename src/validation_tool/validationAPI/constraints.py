from angr import SimProcedure


#Restrictions
#------------------------------------------------------
RESTR_MAP = []
RESTR_COUNTER = 0


class solver_EQ(SimProcedure):
	def run(self, sym_var_addr, sym_var2_addr, length):
		global RESTR_COUNTER
		return_value = RESTR_COUNTER
		RESTR_COUNTER += 1

		sym_var = self.state.memory.load(sym_var_addr, length/8, endness='Iend_LE')
		sym_var2 = self.state.memory.load(sym_var2_addr, length/8, endness='Iend_LE')

		result = (sym_var == sym_var2)
		RESTR_MAP.append(result)

		self.ret(return_value)


class solver_NEQ(SimProcedure):
	def run(self, sym_var_addr, sym_var2_addr, length):
		global RESTR_COUNTER
		return_value = RESTR_COUNTER
		RESTR_COUNTER += 1

		sym_var = self.state.memory.load(sym_var_addr, length/8, endness='Iend_LE')
		sym_var2 = self.state.memory.load(sym_var2_addr, length/8, endness='Iend_LE')

		result = (sym_var != sym_var2)

		RESTR_MAP.append(result)
		self.ret(return_value)



class solver_LT(SimProcedure):
	def run(self, sym_var_addr, sym_var2_addr, length):
		global RESTR_COUNTER
		return_value = RESTR_COUNTER
		RESTR_COUNTER += 1

		sym_var = self.state.memory.load(sym_var_addr, length/8, endness='Iend_LE')
		sym_var2 = self.state.memory.load(sym_var2_addr, length/8, endness='Iend_LE')

		result = sym_var.ULT(sym_var2) 

		RESTR_MAP.append(result)
		self.ret(return_value)


class solver_LE(SimProcedure):
	def run(self, sym_var_addr, sym_var2_addr, length):
		global RESTR_COUNTER
		return_value = RESTR_COUNTER
		RESTR_COUNTER += 1

		sym_var = self.state.memory.load(sym_var_addr, length/8, endness='Iend_LE')
		sym_var2 = self.state.memory.load(sym_var2_addr, length/8, endness='Iend_LE')

		result = sym_var.ULE(sym_var2) 

		RESTR_MAP.append(result)
		self.ret(return_value)


class solver_SLE(SimProcedure):
	def run(self, sym_var_addr, sym_var2_addr, length):
		global RESTR_COUNTER
		return_value = RESTR_COUNTER
		RESTR_COUNTER += 1

		sym_var = self.state.memory.load(sym_var_addr, length/8, endness='Iend_LE')
		sym_var2 = self.state.memory.load(sym_var2_addr, length/8, endness='Iend_LE')

		result = sym_var.SLE(sym_var2) 

		RESTR_MAP.append(result)
		self.ret(return_value)


class solver_SLT(SimProcedure):
	def run(self, sym_var_addr, sym_var2_addr, length):
		global RESTR_COUNTER
		return_value = RESTR_COUNTER
		RESTR_COUNTER += 1

		sym_var = self.state.memory.load(sym_var_addr, length/8, endness='Iend_LE')
		sym_var2 = self.state.memory.load(sym_var2_addr, length/8, endness='Iend_LE')

		result = sym_var.SLT(sym_var2) 

		RESTR_MAP.append(result)
		self.ret(return_value)


#-------------------------------------------------------------------
class solver_NOT(SimProcedure):
	def run(self, restriction):
		global RESTR_COUNTER
		return_value = RESTR_COUNTER
		RESTR_COUNTER += 1
	
		restr_id = self.state.solver.eval(restriction)
		restr = RESTR_MAP[restr_id]
		
		result = self.state.solver.Not(restr)

		RESTR_MAP.append(result)
		self.ret(return_value)


class solver_Or(SimProcedure):
	def run(self, restriction1, restriction2):
		global RESTR_COUNTER
		return_value = RESTR_COUNTER
		RESTR_COUNTER += 1

		restr_id1 = self.state.solver.eval(restriction1)
		restr1 = RESTR_MAP[restr_id1]

		restr_id2 = self.state.solver.eval(restriction2)
		restr2 = RESTR_MAP[restr_id2]

		result = self.state.solver.Or(restr1, restr2)

		RESTR_MAP.append(result)
		self.ret(return_value)


class solver_And(SimProcedure):
	def run(self, restriction1, restriction2):
		global RESTR_COUNTER
		return_value = RESTR_COUNTER
		RESTR_COUNTER += 1

		restr_id1 = self.state.solver.eval(restriction1)
		restr1 = RESTR_MAP[restr_id1]

		restr_id2 = self.state.solver.eval(restriction2)
		restr2 = RESTR_MAP[restr_id2]
		
		result = self.state.solver.And(restr1, restr2)

		RESTR_MAP.append(result)
		self.ret(return_value)


class solver_ITE(SimProcedure):
	def run(self, restr_if_id, restr_then_id, restr_else_id):
		global RESTR_COUNTER
		return_value = RESTR_COUNTER
		RESTR_COUNTER += 1

		restr_if_id = self.state.solver.eval(restr_if_id)
		restr_then_id = self.state.solver.eval(restr_then_id)
		restr_else_id = self.state.solver.eval(restr_else_id)
	
		restr_if = RESTR_MAP[restr_if_id]
		restr_then = RESTR_MAP[restr_then_id]
		restr_else = RESTR_MAP[restr_else_id]

		result = self.state.solver.If(restr_if, restr_then, restr_else)

		RESTR_MAP.append(result)
		self.ret(return_value)


class solver_ITE_VAR(SimProcedure):
	def run(self, restr, sym1, sym2, length1, length2):

		restr = self.state.solver.eval(restr)
	
		restr_if = RESTR_MAP[restr]

		sym_var1 = self.state.memory.load(sym1, length1/8, endness='Iend_LE')
		sym_var2 = self.state.memory.load(sym2, length2/8, endness='Iend_LE')
			
		result = self.state.solver.If(restr_if, sym_var1, sym_var2)

		# result = result.zero_extend(self.state.arch.bits - result.size())

		try:
			self.ret(result)
		except Exception as e:
			print(e)


#--------------------------------------------------------------
class solver_Concat(SimProcedure):
	
	'''
       Concat two symvars
    '''
	
	def run(self,sym_var_addr, sym_var2_addr, length1, length2):

		sym_var = self.state.memory.load(sym_var_addr, length1/8, endness='Iend_LE')
		sym_var2 = self.state.memory.load(sym_var2_addr, length2/8, endness='Iend_LE')
		result = sym_var.concat(sym_var2)

		self.ret(result)
		

class solver_SignExt(SimProcedure):

	'''
		Sign extends a symvar
	'''

	def run(self, sym_var_addr, to_extend, length):
		to_extend = self.state.solver.eval(to_extend)
		sym_var = self.state.memory.load(sym_var_addr, length/8, endness='Iend_LE')
		result = sym_var.sign_extend(to_extend)

		self.ret(result) 


class solver_ZeroExt(SimProcedure):
    
	'''
        Zero extends a symvar
    '''

	def run(self, sym_var_addr, to_extend, length):

		to_extend = self.state.solver.eval(to_extend)
		sym_var = self.state.memory.load(sym_var_addr, length/8, endness='Iend_LE')
		result = sym_var.zero_extend(to_extend)

		self.ret(result) 


class solver_Extract(SimProcedure):
	
	'''
        Extract a portion of the bits of a symvar Bitvec
    '''

	def run(self, sym_var_addr, start, end, length):

		start = self.state.solver.eval(start)
		end = self.state.solver.eval(end)
		sym_var = self.state.memory.load(sym_var_addr, length/8, endness='Iend_LE')

		result = sym_var[end-1:start]

		self.ret(result) 