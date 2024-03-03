#!/usr/bin/env python3
import traceback
import inspect
import logging
import psutil
import signal
import time
import json
import sys
import os

from angr import Project, SimState, SimulationManager, SimHeapPTMalloc
from angr import options, BP_AFTER

from .validationAPI import validation as Validation_API
from .validationAPI import solver as Solver_API
from .validationAPI import constraints as Constraints_API

from .summaries import General as Summaries, CaseStudies as CaseStudies

from .utils import truncate, write2file, get_fnames
from .macros import SYM_VAR 


class angrEngine():
	
	def __init__(self, binary:str, timeout:30*60,
				  save_stats=False, save_paths=False,
				  stats_dir='.', paths_dir='.',
				  convert_ascii=False,
				  ignore=None, debug=False) -> None:
		
		self.binary = os.path.normpath(binary)
		self.timeout = timeout
		
		self.save_paths = save_paths
		self.save_stats = save_stats
		
		self.stats_dir = stats_dir
		self.paths_dir = paths_dir
		
		self.convert_ascii = convert_ascii
		self.ignore_list = self._ignore_list(ignore)
		
		self.binary_name = os.path.split(self.binary)[1]

		self.debug = debug
	
		self.fnames = get_fnames(self.binary)
		self.fcalled = {}

		self.sm: SimulationManager = None

	def _ignore_list(self, ignore):
		f = open(ignore, 'r')
		implemented = f.readlines()
		return [f.strip() for f in implemented]

	
	#Hook API symbols
	def _set_hooks(self, p:Project):

		summs = [Solver_API, Constraints_API, Summaries, CaseStudies]
		
		for s in summs:
			for name, obj in inspect.getmembers(s, inspect.isclass):
					p.hook_symbol(name, obj)

		#Validation
		p.hook_symbol('halt_all', Validation_API.halt_all(self.sm))
		p.hook_symbol('mem_addr', Validation_API.mem_addr())
		p.hook_symbol('save_current_state', Validation_API.save_current_state())
		p.hook_symbol('get_cnstr', Validation_API.get_cnstr())
		p.hook_symbol('store_cnstr', Validation_API.store_cnstr())
		p.hook_symbol('check_implications', Validation_API.check_implications())
		p.hook_symbol('print_counterexamples', Validation_API.print_counterexamples(self.binary_name, self.stats_dir, self.convert_ascii))

	
	def _create_entry_state(self, p:Project) -> SimState:

		opt = {options.TRACK_SOLVER_VARIABLES,
			options.ZERO_FILL_UNCONSTRAINED_MEMORY,
			options.ZERO_FILL_UNCONSTRAINED_REGISTERS}

		state = p.factory.entry_state(mode='symbolic', add_options=opt)

		if state.arch.bits == 64:
			heap = SimHeapPTMalloc(heap_base=0x0000000000000000)
		else:
			heap = SimHeapPTMalloc()
		state.register_plugin('heap', heap)
		
		state.libc.simple_strtok = False
		
		if self.save_stats:
			state.inspect.b('call', when=BP_AFTER, action=self._count_fcall)

		return state

	def _register_timeout(self):

		def handler(signum, frame):
			if self.save_stats:
				self._save_stats(timeout=True)
			print(f'[!] Timeout Detected {self.timeout} seconds')
			sys.exit(0)

		signal.signal(signal.SIGALRM, handler)
		signal.alarm(self.timeout)


	def _get_states(self, sm:SimulationManager):
		states = sm.deadended + sm.active
		return states


	def _count_fcall(self, state):
		addr = str(state.inspect.function_address) 	#<BV32 0x80483a3>
		addr = addr.split()[1] 			 		 	#0x80483a3>
		addr = addr[:-1]					  		#0x80483a3
		addr = addr[2:]								#80483a3

		if addr in self.fcalled.keys():
			self.fcalled[addr] += 1
		else:
			self.fcalled[addr] = 1


	def _save_paths(self, sm:SimulationManager):
	
		def filter_gen(var):
			if SYM_VAR in str(var):
				return True
			return False

		# Create results folder if it does not exist yet
		if not os.path.exists(self.paths_dir):
			os.makedirs(self.paths_dir)
		
		for idx, state in enumerate(self._get_states(sm)):
			file = f'{self.paths_dir}/{self.binary_name}_{idx}.path'
			truncate(file)
			
			vars = state.solver.all_variables
			vars = list(filter(filter_gen, vars))	
			
			for var in vars:
				v = state.solver.eval(var)
				write2file(file, v)
		return

	def _save_stats(self, time_spent=None, timeout=None,
				  	start=None,
				    exception=None):
		
		out_stats = {}

		# Create results folder if it does not exist yet
		if not os.path.exists(self.stats_dir):
			os.makedirs(self.stats_dir)
		
		if exception:
			assert start is not None
			time_spent = round(time.time()-start, 4)
			out_stats['Exception'] = f'{type(exception)}:{exception}'
		
		elif timeout:
			out_stats['Time'] = f'Timeout:{timeout}'
		
		else:
			assert time_spent is not None
			out_stats['Time'] = time_spent

		# out_stats['T_Solver'] = round(claripy.SOLVER_TIME, 4)
		out_stats['N_Paths'] = len(self._get_states())
		
		#Convert function call addrs to symbols
		converted = {}
		for f in self.fcalled.keys():
			if f in self.fnames.keys():
				fname = self.fnames[f]
				converted[fname] = self.fcalled[f]

		out_stats['Fcalled'] = converted
		out_stats['Fcalled'].pop('main', None)
		
		out_stats = {self.binary_name:out_stats}

		file = open(f'{self.stats_dir}/{self.binary_name}_stats.json', 'w')
		json_object = json.dumps(out_stats, indent = 2)
		file.write(json_object)
		file.flush()
		file.close()


	def _step(self, sm:SimulationManager, start:float):
		try:
			while sm.active:
				if psutil.virtual_memory().percent > 50:
					raise MemoryError
				sm.step()
		
		except Exception as e:
			
			if self.save_stats:
				self._save_stats(exception=e, start=start)
			
			print(traceback.format_exc())
			sys.exit(1)


	def run(self):
		
		if self.debug:
			logging.getLogger('angr').setLevel('INFO')	

		sys.setrecursionlimit(20000)
		self._register_timeout()
		
		p = Project(self.binary, exclude_sim_procedures_list=self.ignore_list)

		state = self._create_entry_state()
		sm = p.factory.simulation_manager(state)
		self.sm = sm

		# Set hooks after creating simulation manager
		# self.sm is passed to one of the hooks
		self._set_hooks(p)

		#Run Symbolic Execution
		start = time.time()
		self._step(sm)
		end = time.time()

		#Store execution time
		tspent = round(end-start, 4)

		if self.save_stats:
			self._save_stats(time_spent=tspent)

		if self.save_paths:
			self._save_paths()