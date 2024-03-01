#!/usr/bin/env python3

import sys
import traceback
from argparse import Namespace

from input_options import parse_input_args
from validation_gen import ValidationGenerator, CCompiler


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
	summ_name = args.summ_name
	func_name = args.func_name
	outputfile = args.o

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
				    					arraysize=args.arraysize, nullbytes=args.nullbytes,
										maxnum=args.maxvalue, maxnames=args.maxnames,
										default=args.defaultvalues, concrete_arrays=args.concretearray,
									    memory=args.memory,
										cncrt_name=func_name, summ_name=summ_name,
										no_api=args.noAPI)
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