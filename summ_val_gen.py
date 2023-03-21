#!/usr/bin/env python3

import argparse
import sys
import ast
import re

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

	parser.add_argument('--arraysize', metavar='value | [val1,val2]', nargs='+', type=int, required=False, default=[5],
						help='Maximum array size of each test (default:5)')

	parser.add_argument('--nullbytes', metavar='index | [idx1,idx2]', nargs='+', type=int, required=False, default=[],
						help='Specify array indexes to place null bytes')

	parser.add_argument('--defaultvalues', metavar='{var:value}', nargs='+', type=int, required=False, default={},
						help='Specify default const values for input variables')

	parser.add_argument('--maxvalue', metavar='value', nargs='+', type=int, required=False, default=[],
						help='Provide an upper bound for numeric values')

	parser.add_argument('--maxnames', metavar='name', nargs='+', type=int, required=False, default=[],
						help='Numeric value names to be constrained')
	
	parser.add_argument('--concretearray', metavar='{var:[indexes]}', nargs='+', type=int, required=False, default={},
						help='Place concrete values in selected array indexes')

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


def parse_config_dict(line):
	
	if '{' in line:
		value_sets  = re.findall(r'(\{[^\}]*\})+', line)
		return [s for s in map(lambda x: ast.literal_eval(x), value_sets)]

def parse_config_list(line):
	
	if '[' in line:
		size_sets  = re.findall(r'(\[[^\]]*\])+', line)
		return [s for s in map(lambda x: ast.literal_eval(x), size_sets)]

	else:
		split = line.split(' ')
		return [size for size in map(lambda x: int(x), split[1:])]



def parse_config(conf) -> dict:
	f = open(conf, "r")
	lines = f.readlines()
	f.close()

	config = {}

	for l in lines:
		l = l.strip()

		if l.startswith('//'):
			continue

		split = l.split(' ')
		if 'array_size' in split[0]:
			config['array_size'] = parse_config_list(l)

		if 'null_bytes' in split[0]:
			config['null_bytes'] = parse_config_list(l)

		if 'max_num' in split[0]:
			config['max_num'] = [size for size in map(lambda x: int(x), split[1:])]

		if 'summ_name' in split[0]:
			if len(split) == 2:
				config['summ_name'] = split[1]

		if 'func_name' in split[0]:
			if len(split) == 2:
				config['func_name'] = split[1]
		
		if 'compile_arch' in split[0]:
			if len(split) == 2:
				config['compile_arch'] = split[1]
		
		if 'summ_file' in split[0]:
			if len(split) == 2:
				config['summ_file'] = split[1]

		if 'func_file' in split[0]:
			if len(split) == 2:
				config['func_file'] = split[1]				

		if 'lib' in split[0]:
			if len(split) == 2:
				config['lib'] = split[1]

		if 'max_names' in split[0]:
			config['max_names'] = [n for n in split[1:]]

		if 'default_values' in split[0]:
			config['default_values'] = parse_config_dict(l)

		if 'concrete_array' in split[0]:
			config['concrete_array'] = parse_config_dict(l)

	return config



if __name__ == "__main__":
	
	#Command line arguments
	args = get_cmd_args()
	
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
	compile_arch = args.compile
	lib_paths = args.lib
	memory = args.memory
	config_file = args.config
	noapi = args.noAPI
	
	if '[' in arraysize:
		arraysize = [s for s in map(lambda x: ast.literal_eval(x), arraysize)]

	if '[' in nullbytes:
		nullbytes = [s for s in map(lambda x: ast.literal_eval(x), nullbytes)]

	if '[' in default_values:
		default_values = [s for s in map(lambda x: ast.literal_eval(x), default_values)]

	if '[' in concrete_array:
		concrete_array = [s for s in map(lambda x: ast.literal_eval(x), concrete_array)]

	if config_file:
		
		config = parse_config(config_file)
		keys = config.keys()

		if 'array_size' in keys:
			arraysize = config['array_size']

		if 'null_bytes' in keys:
			nullbytes = config['null_bytes']

		if 'max_num' in keys:
			maxvalue = config['max_num']

		if 'summ_name' in keys:
			summ_name = config['summ_name']			

		if 'func_name' in keys:
			func_name = config['func_name']			
		
		if 'compile_arch' in keys:
			compile_arch = config['compile_arch']		

		if 'summ_file' in keys:
			target_summary = config['summ_file']	

		if 'func_file' in keys:
			concrete_function = config['func_file']	
		
		if 'lib' in keys:
			lib_paths = config['lib']	

		if 'max_names' in keys:
			max_names = config['max_names']

		if 'default_values' in keys:
			default_values = config['default_values']
		
		if 'concrete_array' in keys:
			concrete_array = config['concrete_array']


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

	if compile_arch:
		bin_name = outputfile[:-2] + '.test' #Remove '.c' + .test
		comp = CCompiler(compile_arch, outputfile, bin_name, lib_paths)
		comp.compile()
