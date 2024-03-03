import ast
import argparse

from options import Options, OptionTypes
from config_file import parse_config_file

def parse_cmd_args(input=None):

	def flag(option:tuple):
		return f'{option[0]}{option[1]}'

	parser = argparse.ArgumentParser(prog='summvb', description='Generate Summary Validation Tests')

	parser.add_argument(flag(Options.o), metavar='name', type=str, required=False, default='test.c',
						help='Test output name')

	parser.add_argument(flag(Options.func) , metavar='file', type=str,
						help='Path to file containing the concrete function')

	parser.add_argument(flag(Options.summ), metavar='file', type=str,
						help='Path to file containing the target summary')

	parser.add_argument(flag(Options.summname), metavar='name', type=str,
						help='Name of the summary in the given path')
	
	parser.add_argument(flag(Options.funcname), metavar='name', type=str,
						help='Name of the concrete function in the given path')

	parser.add_argument(flag(Options.arraysize), metavar='value | [val1,val2]', nargs='+', required=False, default=[5],
						help='Maximum array size of each test (default:5)')

	parser.add_argument(flag(Options.nullbytes), metavar='index | [idx1,idx2]', nargs='+', required=False, default=[],
						help='Specify array indexes to place null bytes')

	parser.add_argument(flag(Options.defaultvalues), metavar='{var:value}', nargs='+', required=False, default={},
						help='Specify default const values for input variables')

	parser.add_argument(flag(Options.maxvalue), metavar='value', nargs='+', required=False, default=[],
						help='Provide an upper bound for numeric values')

	parser.add_argument(flag(Options.maxnames), metavar='name', nargs='+', required=False, default=[],
						help='Numeric value names to be constrained')
	
	parser.add_argument(flag(Options.concretearray), metavar='{var:[indexes]}', nargs='+', required=False, default={},
						help='Place concrete values in selected array indexes')

	parser.add_argument(flag(Options.lib), metavar='path', nargs='+', type=str, required=False,
						help='Path to external files needed to compile the test binary')

	parser.add_argument(flag(Options.noapi), action='store_true',
						help='Do not include the Validation API stubs')

	parser.add_argument(flag(Options.compile), const='x86', choices=['x86', 'x64'], nargs='?',
						help='Compile the generated test')
	
	parser.add_argument(flag(Options.memory), action='store_true',
						help='Evaluate a summary with memory manipulation side-effects')

	parser.add_argument(flag(Options.config), metavar='path', type=str, required=False,
						help='Config file')

	args = parser.parse_args(input)

	assert len(vars(args)) == len(vars(Options))
	return args


def eval_ast(array):
	if array and isinstance(array[0], str):
		if '[' in array[0] or '{' in array[0]:
			return list(map(lambda x: ast.literal_eval(x), array))
	return array

def parse_input_args(input=None):

	# Parse command line args
	args = parse_cmd_args(input)
	options = Options.values()
	complex = [OptionTypes.NESTED, OptionTypes.DICT]

	#Convert complex options string to Python ast
	for arg in filter(lambda a: a[2] in complex, options):
		parsed = eval_ast(getattr(args, arg[1]))
		setattr(args, arg[1], parsed)

	# Parse config file and override cmd args
	config_file = args.config
	if config_file:
		
		config = parse_config_file(config_file)
		for c in config.keys():
			setattr(args, c, config[c])
			
	return args