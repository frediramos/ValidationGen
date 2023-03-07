import os, traceback

from pycparser import c_generator
from pycparser.c_ast import *

from . CGenerator import CGenerator
from SummValidation.APIGen import API_Gen
from SummValidation.APIGen import API
from SummValidation.TestGen import TestGen

from SummValidation.Utils import * 
from SummValidation.FParser import FunctionException
from SummValidation.FParser import FunctionParser


class ValidationGenerator(CGenerator):
	def __init__(self, concrete_file, summary_file,
				 outputfile,
				 arraysize = [5], maxnum = [],
				 memory = False,
				 cncrt_name = None, summ_name=None, no_api=False,
				 fakelib=None):

		super().__init__(outputfile, concrete_file, summary_file, fakelib)

		self.arraysize = arraysize
		self.maxnum = maxnum
		self.memory = memory

		#Summary name (if summ is not isolated in a file, e,g in a library)
		self.summ_name = summ_name
		self.cncrt_name = cncrt_name

		self.no_api = no_api


	#Gen headers
	#Typedefs, API stubs and Macros
	def _gen_headers(self, defs):
		_ , summ_def = defs

		#Add core api functions
		headers = []

		if not self.no_api:
			headers += API.type_defs
			headers += API.validation_api.values()
			headers.append('\n')

			#Visitor to get all function calls
			call_vis = FCallsVisitor()
			call_vis.visit(summ_def)
			calls = call_vis.fcalls()

			#Check if calls are api functions
			#Only add stubs for functions not already added by API.validation_api
			for c in calls:
				if c in API.all_api.keys():
					stub = API.all_api[c]
					if c not in API.validation_api:
						headers.append(stub)
			headers.append('\n')

		#Array size macros
		i = 0
		for size in self.arraysize:	
			i += 1	
			headers.append(defineMacro(f'{ARRAY_SIZE_MACRO}_{i}', size))
		
		#Max numeric value macros
		j = 0
		for max in self.maxnum:	
			j += 1	
			headers.append(defineMacro(f'{MAX_MACRO}_{j}', max))

		return headers


	#Generate the tests code
	def _gen_tests(self, args, ret_type):

		#Gen helpers
		api_gen = API_Gen()	
		test_gen = TestGen(args, ret_type, self.cncrt_name, self.summ_name, self.memory)

		test_defs = []
		main_body = []

		array_size = f'{ARRAY_SIZE_MACRO}_1' #There is always one default size macro

		#Number of tests
		tests = max(len(self.maxnum),len(self.arraysize))

		for i in range(1, tests):	
	
			main_body.append(api_gen.save_current_state(f'fresh_state{i}'))
		
		for i in range(1, tests+1):	
			
			#Create test name
			test_name = f'test_{i}'

			if i <= len(self.arraysize):
				array_size = f'{ARRAY_SIZE_MACRO}_{i}'

			max_value = None
			if i <= len(self.maxnum):
				max_value = f'{MAX_MACRO}_{i}'

			#Gen test using helper
			test_defs.append(test_gen.createTest(test_name, array_size, max_value, i))
			
			#Call test function from main
			main_body.append(FuncCall(ID(test_name), ExprList([])))

			#Halt to a fresh state in between tests
			if i < tests:
				main_body.append(api_gen.halt_all(f'fresh_state{i}')) 
		
		return test_defs, main_body


	#Generate summary validation test
	def gen(self):
		try:
			tmp_concrete = self.add_fake_include(self.concrete_file)
			tmp_summary = self.add_fake_include(self.summary_file)

			try:
				fparser = FunctionParser(tmp_concrete, tmp_summary)
				
				cname, sname, function_defs, args, ret_type = \
					  fparser.parse(self.cncrt_name, self.summ_name)
				
				self.cncrt_name = cname
				self.summ_name = sname
				header = self._gen_headers(function_defs)	
						
			except FunctionException as e:
				self.exit(str(e))

			#Main function to run the tests	
			main = createFunction(name='main',args=None, returnType='int')
			
			#Gen test definitions and calls from main
			test_defs, main_body = self._gen_tests(args, ret_type)

			block = Compound(main_body)
			main_ast = FuncDef(main, None, block, None)
		
			gen_ast = FileAST(function_defs + test_defs)
			gen_ast.ext.append(main_ast)


			#Generate string from ast
			generator = c_generator.CGenerator()
			generated_string = generator.visit(gen_ast)

			file_name = os.path.basename(__file__)
			self.write_to_file(generated_string, header, file_name)
			self.remove_files(tmp_concrete, tmp_summary)
			return self.outputfile

		except Exception:
			self.remove_files(tmp_concrete, tmp_summary)
			print(traceback.format_exc())
			return None

