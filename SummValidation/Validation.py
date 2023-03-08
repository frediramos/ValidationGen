import os, traceback

from pycparser import c_generator
from pycparser.c_ast import *

from . CGenerator import CGenerator
from SummValidation.Utils import * 
from SummValidation.APIGen import API_Gen
from SummValidation.APIGen import API
from SummValidation.FParser import FunctionException
from SummValidation.FParser import FunctionParser
from SummValidation.TestGen import TestGen
from SummValidation.TestGen.ArgGen.Visitors.Structs import StructVisitor


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
	def gen_headers(self, defs):
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
			calls = filter(lambda x: x in API.all_api.keys(), calls)
			calls = filter(lambda x: x not in API.validation_api, calls)

			headers += [API.all_api[c] for c in calls]
			headers.append('\n')
			
		#Macros
		headers += self.genMacros(ARRAY_SIZE_MACRO, self.arraysize)
		headers += self.genMacros(MAX_MACRO, self.maxnum)

		return headers

	

	def genMacros(self, macro, values =[]):
		macros = []
		for i, v in enumerate(values):
			string = defineMacro(f'{macro}_{i+1}', v)
			macros.append(string)		
		return macros


	#Generate the tests code
	def genTests(self, args, ret_type):

		test_defs = []
		main_body = []

		#Number of tests
		tests = max(len(self.maxnum),len(self.arraysize))

		#Save Multiple fresh states if needed (multiple tests)
		main_body += [API_Gen().save_current_state(f'fresh_state{i}')
					 for i in range(1,tests)]

		for i in range(1, tests+1):	
			testName = f'test_{i}'

			#Gen test code
			testCode = self.genTest(testName, args, ret_type, i)
			test_defs.append(testCode)
			
			#Call test function from main
			main_body.append(FuncCall(ID(testName), ExprList([])))

			#Halt to a fresh state in between tests
			if i < tests:
				main_body.append(API_Gen().halt_all(f'fresh_state{i}')) 
		
		return test_defs, main_body


	def genTest(self, testname, args, ret_type, id):
		
		#Select Macro id for arraysize
		arrId = min(id, len(self.arraysize))
		array_size = f'{ARRAY_SIZE_MACRO}_{arrId}'

		#Select Macro id for Max value
		max_value = f'{MAX_MACRO}_{id}' if id <= len(self.maxnum) else None

		#Call Gen visitor
		gen = TestGen(args, ret_type,
		 		self.cncrt_name, self.summ_name,
		   		self.memory)

		return gen.createTest(testname, array_size, max_value, id)
			


	#Generate summary validation test
	def gen(self):
		try:

			try:
				fparser = FunctionParser(self.tmp_concrete, self.tmp_summary)
				cname, sname,	\
				function_defs, args,	\
				ret_type = fparser.parse(self.cncrt_name, self.summ_name)
				
				self.cncrt_name = cname
				self.summ_name = sname
				header = self.gen_headers(function_defs)	
						
			except FunctionException as e:
				self.exit(str(e))

			#Main function to run the tests	
			main = createFunction(name='main',args=None, returnType='int')
			
			#Gen test definitions and calls from main
			test_defs, main_body = self.genTests(args, ret_type)

			#Struct builder functions (if exist)
			structs =  StructVisitor(self.tmp_concrete).symbolic_structs()
			structs +=  StructVisitor(self.tmp_summary).symbolic_structs()

			#Create main() body
			block = Compound(main_body)
			main_ast = FuncDef(main, None, block, None)
		
			gen_ast = FileAST(structs + function_defs + test_defs)
			gen_ast.ext.append(main_ast)

			#Generate string from ast
			generator = c_generator.CGenerator()
			generated_string = generator.visit(gen_ast)

			file_name = os.path.basename(__file__)
			self.write_to_file(generated_string, header, file_name)
			self.remove_files(self.tmp_concrete, self.tmp_summary)
			return self.outputfile

		except Exception:
			self.remove_files(self.tmp_concrete, self.tmp_summary)
			print(traceback.format_exc())
			return None

