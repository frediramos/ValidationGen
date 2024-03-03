class OptionTypes:

	BOOL   = 'boolean'
	SIMPLE = 'simple'
	LIST   = 'list' 
	NESTED = 'nested'
	DICT   = 'dict'

class Options():

	def __init__(self) -> None:
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

	def values(self):
		return list(self.__dict__.values())

	def names(self):
		return [arg[1] for arg in self.__dict__.values()]

Options = Options()
