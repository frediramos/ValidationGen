#!/usr/bin/env python3

import ast
import sys
import traceback
from argparse import Namespace

from SummValidation import ValidationGenerator, CCompiler

from input_options import parse_input_args


def compileValidationTest(arch, file:str, libs):
	bin_name = file[:-2] + '.test' #Remove '.c' + .test
	comp = CCompiler(arch, file, bin_name, libs)
	comp.compile()
	return bin_name


#Takes command line / config file arguments
def runValidationGen(args: Namespace):
	'''
	Take command line args and run the test generation
	@args: \'argparse\' Namespace object
	'''
	concrete_function = args.func
	target_summary = args.summ
	outputfile = args.o
	arraysize = args.arraysize
	nullbytes = args.nullbytes
	concrete_array = args.concretearray
	maxvalue = args.maxvalue
	max_names = args.maxnames
	summ_name = args.summ_name
	func_name = args.func_name
	default_values = args.defaultvalues
	memory = args.memory
	noapi = args.noAPI
	

	if not concrete_function and not target_summary:
		sys.exit('ERROR: At least the code for a concrete function or summary MUST be provided')

	if not concrete_function and not func_name:
		msg = ("ERROR: No concrete function code or name provided\n"
				"INFO: In the absence of the code, a name must be specified in order to call the function")
		sys.exit(msg)

	if not target_summary and not summ_name:
		msg = ("ERROR: No summary code or name provided\n"
				"INFO: In the absence of the code, a name must be specified in order to call the summary")
		sys.exit(msg)


	valgenerator = ValidationGenerator(concrete_function, target_summary, outputfile,
				    					arraysize=arraysize, nullbytes=nullbytes,
										maxnum=maxvalue, maxnames=max_names,
										default=default_values, concrete_arrays=concrete_array,
									    memory=memory,
										cncrt_name=func_name, summ_name=summ_name,
										no_api=noapi)
	file = valgenerator.gen()

	assert(file == outputfile)
	return file


def main():
	try:
		args = parse_input_args()
		test = runValidationGen(args)
		if args.compile:
			arch = args.compile
			libs = args.lib
			compileValidationTest(arch, test, libs)

	except Exception:
		print(traceback.format_exc(), end='')
		return 1
	return 0

if __name__ == "__main__":
	sys.exit(main())