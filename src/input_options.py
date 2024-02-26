import re
import ast
import argparse

def parse_cmd_args(args=None):
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

	parser.add_argument('--arraysize', metavar='value | [val1,val2]', nargs='+', required=False, default=[5],
						help='Maximum array size of each test (default:5)')

	parser.add_argument('--nullbytes', metavar='index | [idx1,idx2]', nargs='+', required=False, default=[],
						help='Specify array indexes to place null bytes')

	parser.add_argument('--defaultvalues', metavar='{var:value}', nargs='+', required=False, default={},
						help='Specify default const values for input variables')

	parser.add_argument('--maxvalue', metavar='value', nargs='+', required=False, default=[],
						help='Provide an upper bound for numeric values')

	parser.add_argument('--maxnames', metavar='name', nargs='+', required=False, default=[],
						help='Numeric value names to be constrained')
	
	parser.add_argument('--concretearray', metavar='{var:[indexes]}', nargs='+', required=False, default={},
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

	return parser.parse_args(args)



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



def parse_config_file(conf) -> dict:
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
			assert '[' not in l
			config['max_num'] = parse_config_list(l)

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
			assert '[' not in l
			config['lib'] = parse_config_list(l)

		if 'max_names' in split[0]:
			config['max_names'] = [n for n in split[1:]]

		if 'default_values' in split[0]:
			config['default_values'] = parse_config_dict(l)

		if 'concrete_array' in split[0]:
			config['concrete_array'] = parse_config_dict(l)

	return config


def parse_input_args(args=None):

	# Parse command line args
	args = parse_cmd_args(args)

	arraysize = args.arraysize
	nullbytes = args.nullbytes
	concrete_array = args.concretearray
	default_values = args.defaultvalues
	config_file = args.config
	
	if isinstance(arraysize[0], str) and '[' in arraysize[0]:
		args.arraysize = [s for s in map(lambda x: ast.literal_eval(x), arraysize)]

	if isinstance(arraysize[0], str) and '[' in nullbytes[0]:
		args.nullbytes = [s for s in map(lambda x: ast.literal_eval(x), nullbytes)]

	if isinstance(arraysize[0], str) and  '[' in default_values[0]:
		args.defaultvalues = [s for s in map(lambda x: ast.literal_eval(x), default_values)]

	if isinstance(arraysize[0], str) and  '[' in concrete_array[0]:
		args.concretearray = [s for s in map(lambda x: ast.literal_eval(x), concrete_array)]

	# Parse config file
	if config_file:
		
		config = parse_config_file(config_file)
		keys = config.keys()

		if 'array_size' in keys:
			args.arraysize = config['array_size']

		if 'null_bytes' in keys:
			args.nullbytes = config['null_bytes']

		if 'max_num' in keys:
			args.maxvalue = config['max_num']

		if 'summ_name' in keys:
			args.summ_name = config['summ_name']			

		if 'func_name' in keys:
			args.func_name = config['func_name']			
		
		if 'compile_arch' in keys:
			args.compile = config['compile_arch']		

		if 'summ_file' in keys:
			args.summ = config['summ_file']	

		if 'func_file' in keys:
			args.func = config['func_file']	
		
		if 'lib' in keys:
			args.lib = config['lib']	

		if 'max_names' in keys:
			args.max_names = config['max_names']

		if 'default_values' in keys:
			args.defaultvalues = config['default_values']
		
		if 'concrete_array' in keys:
			args.concretearray = config['concrete_array']
	
	return args