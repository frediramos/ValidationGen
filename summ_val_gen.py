#!/usr/bin/env python3

import argparse
import sys
from SummValidation import ValidationGenerator, CCompiler


def get_cmd_args():
	parser = argparse.ArgumentParser(description='Generate Summary Validation Tests')

	parser.add_argument('-o', metavar='name', type=str, required=False, default='test.c',
						help='Test output name')

	parser.add_argument('-func', metavar='file', type=str,
						help='Path to file containing the concrete function')

	parser.add_argument('-summ', metavar='file', type=str,
						help='Path to file containing the target summary')

	parser.add_argument('--summ_name', metavar='name', type=str,
						help='Name of the summary in the given path')
	
	parser.add_argument('--func_name', metavar='name', type=str,
						help='Name of the concrete function in the given path')

	parser.add_argument('--arraysize', metavar='value', nargs='+', type=int, required=False, default=[5],
						help='Maximum array size of each test (default:5)')

	parser.add_argument('--maxvalue', metavar='value', nargs='+', type=int, required=False, default=[],
						help='Provide an upper bound for numeric values')

	parser.add_argument('--lib', metavar='path', nargs='+', type=str, required=False,
						help='Path to external files needed to compile the test binary')

	parser.add_argument('-noAPI', action='store_true',
						help='Do not include the Validation API stubs')

	parser.add_argument('--compile', const='x86', choices=['x86', 'x64'], nargs='?',
						help='Compile the generated test')
	
	parser.add_argument('-memory', action='store_true',
						help='Evaluate a summary with memory manipulation side-effects')

	parser.add_argument('-config', metavar='path', type=str, required=False,
						help='Config file')


	return parser.parse_args()


def parse_config(conf):
	f = open(conf, "r")
	lines = f.readlines()
	f.close()

	array_size = None
	max_num = None
	summ_name = None
	func_name = None
	omit = None

	for l in lines:
		l = l.strip()
		split = l.split(' ')
		if 'array_size' in split[0]:
			array_size = [size for size in map(lambda x: int(x), split[1:])]

		if 'max_num' in split[0]:
			max_num = [size for size in map(lambda x: int(x), split[1:])]

		if 'omit' in split[0]:
			omit = [n for n in split[1:]]		

		if 'summ_name' in split[0]:
			if len(split) == 2:
				summ_name = split[1]

		if 'func_name' in split[0]:
			if len(split) == 2:
				func_name = split[1]

	return array_size, max_num, summ_name, func_name, omit

if __name__ == "__main__":

	
	#Command line arguments
	args = get_cmd_args()
	
	concrete_function = args.func
	target_summary = args.summ
	outputfile = args.o
	arraysize = args.arraysize
	maxvalue = args.maxvalue
	summ_name = args.summ_name
	func_name = args.func_name
	compile_arch = args.compile
	lib_paths = args.lib
	memory = args.memory
	config_file = args.config
	noapi = args.noAPI

	if config_file:
		conf_arraysize, conf_maxvalue,\
		conf_summ_name, conf_func_name,\
		conf_omit = parse_config(config_file)

		if conf_arraysize:
			arraysize = conf_arraysize

		if conf_maxvalue:
			maxvalue = conf_maxvalue

		if conf_summ_name:
			summ_name = conf_summ_name			

		if conf_func_name:
			func_name = conf_func_name		

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


	valgenerator = ValidationGenerator(concrete_function, target_summary,
					 			 		outputfile, arraysize,
										maxvalue, memory,
										func_name, summ_name, noapi)
	file = valgenerator.gen()

	assert(file == outputfile)

	if compile_arch:
		bin_name = outputfile[:-2] #Remove '.c'
		comp = CCompiler(compile_arch, outputfile, bin_name, lib_paths)
		comp.compile()
