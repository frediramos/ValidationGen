class OptionTypes:

	BOOL   = 'boolean'
	SIMPLE = 'simple'
	LIST   = 'list' 
	NESTED = 'nested'
	DICT   = 'dict'

class Options():


	# Validate option defs just in case
	# 1 - check that class attributes and option names match
	# 2 - check that all used types are define in OptionTypes 
	def validate_options(self):
		for name, opt in self.__dict__.items():
			optname = opt[1]
			opttype = opt[2]
			assert opttype in vars(OptionTypes).values()
			assert name == optname, f'option names must match => self.{name} != {optname}'


	def __init__(self) -> None:
		
		# Validation Gen
		self.o = ('-', 'o', OptionTypes.SIMPLE)
		self.func = ('-', 'func', OptionTypes.SIMPLE)
		self.summ = ('-', 'summ', OptionTypes.SIMPLE)
		self.summname = ('--', 'summname', OptionTypes.SIMPLE)
		self.funcname = ('--', 'funcname', OptionTypes.SIMPLE)
		self.arraysize = ('--', 'arraysize', OptionTypes.NESTED)
		self.nullbytes = ('--', 'nullbytes', OptionTypes.NESTED)
		self.defaultvalues = ('--', 'defaultvalues', OptionTypes.NESTED)
		self.maxvalue = ('--', 'maxvalue', OptionTypes.LIST)
		self.maxnames = ('--', 'maxnames', OptionTypes.LIST)
		self.concretearray = ('--', 'concretearray', OptionTypes.DICT)
		self.lib = ('--', 'lib', OptionTypes.LIST)
		self.noapi = ('-', 'noapi', OptionTypes.BOOL)
		self.compile = ('--', 'compile', OptionTypes.SIMPLE)
		self.memory = ('-', 'memory', OptionTypes.BOOL)
		self.config = ('-', 'config', OptionTypes.SIMPLE)

		# Validation Run
		self.run = ('-', 'run', OptionTypes.BOOL)
		self.binary = ('--', 'binary', OptionTypes.SIMPLE)
		self.timeout = ('-', 'timeout', OptionTypes.SIMPLE)
		self.results = ('--', 'results', OptionTypes.SIMPLE)
		self.ascii = ('-', 'ascii', OptionTypes.BOOL)
		self.debug = ('-', 'debug', OptionTypes.BOOL)

		self.validate_options()

	def values(self):
		return list(self.__dict__.values())

	def names(self):
		return [opt[1] for opt in self.__dict__.values()]

Options = Options()
