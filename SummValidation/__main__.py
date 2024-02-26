#!/usr/bin/env python3

import argparse

from .FrontEnd import runValidationGen


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


	return parser.parse_args()



if __name__ == "__main__":
	
	#Command line arguments
	args = get_cmd_args()
	runValidationGen(args)