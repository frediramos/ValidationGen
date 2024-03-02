import re
import ast

def parse_config_dict(line):
	
	if '{' in line:
		value_sets  = re.findall(r'(\{[^\}]*\})+', line)
		return list(map(lambda x: ast.literal_eval(x), value_sets))

def parse_config_list(line):
	
	if '[' in line:
		size_sets  = re.findall(r'(\[[^\]]*\])+', line)
		return list(map(lambda x: ast.literal_eval(x), size_sets))

	else:
		split = line.split(' ')
		return list(map(lambda x: int(x), split[1:]))


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
		option = split[0]
		if 'array_size' in option:
			config['array_size'] = parse_config_list(l)

		if 'null_bytes' in option:
			config['null_bytes'] = parse_config_list(l)

		if 'max_num' in option:
			assert '[' not in l
			config['max_num'] = parse_config_list(l)

		if 'summ_name' == option:
			if len(split) == 2:
				config['summ_name'] = split[1]

		if 'func_name' in option:
			if len(split) == 2:
				config['func_name'] = split[1]
		
		if 'compile_arch' in option:
			if len(split) == 2:
				config['compile_arch'] = split[1]
		
		if 'summ' == option:
			if len(split) == 2:
				config['summ'] = split[1]

		if 'func' in option:
			if len(split) == 2:
				config['func'] = split[1]				

		if 'lib' in option:
			assert '[' not in l
			config['lib'] = parse_config_list(l)

		if 'max_names' in option:
			config['max_names'] = [n for n in split[1:]]

		if 'default_values' in option:
			config['default_values'] = parse_config_dict(l)

		if 'concrete_array' in option:
			config['concrete_array'] = parse_config_dict(l)

	return config
