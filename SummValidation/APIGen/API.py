type_defs = [
    '#define NULL ((void*)0)\n'
    '#define INT_SIZE (sizeof(int) * 8)\n',
    '#define LONG_SIZE (sizeof(long) * 8)\n',
    '#define CHAR_SIZE (sizeof(char) * 8)\n',
    '#define PTR_SIZE (sizeof(void*) * 8)\n',
    'typedef void* symbolic; \n',
    'typedef int state_t; \n',
    'typedef unsigned int size_t; \n',
    'typedef unsigned int cnstr_t; \n',
    'typedef unsigned int result_t; \n',
    'typedef unsigned int wchar_t; \n',
    '\n'
]

validation_api = {
    'save_current_state':       'state_t save_current_state() {return 0;} \n',
    'get_cnstr':                'cnstr_t get_cnstr(symbolic var, size_t size) {return 0;} \n',
    'store_cnstr':              'void store_cnstr(char* name, cnstr_t constraint) {return;} \n',
    'halt_all':                 'void halt_all(state_t state) {return;} \n',
    'check_implications':       'result_t check_implications(char* constraint1, char* constraint2) {return 0;} \n',
    'print_counterexamples':    'void print_counterexamples(result_t result) {return;}\n',
    'new_sym_var_named':        'symbolic new_sym_var_named(char* name, size_t size) {return 0;}\n',
    'new_sym_var_array':        'symbolic new_sym_var_array(char* name, size_t index, size_t size) {return 0;}\n',   
    'mem_addr':                 'void mem_addr(char* name, void* addr, size_t length) {return;} \n',
    '_solver_LE':               'cnstr_t _solver_LE(symbolic sym_var, symbolic sym_var2, size_t length) {return 0;} \n',
    'assume':                   'void assume(cnstr_t cnstr) {return;} \n'
}

standard_api = {
    'error':            'void error(char *fname) {return;} \n',
    'assume':           'void assume(cnstr_t cnstr) {return;} \n',
    'is_symbolic':      'int is_symbolic(symbolic sym_var, size_t size) {return 0;} \n',
    'print_byte':       'void print_byte(char byte) {return;} \n',
    'maximize':         'void* maximize(symbolic sym_var, size_t length) {return NULL;} \n',
    'is_sat':           'int is_sat(cnstr_t cnstr) {return 0;}\n'

}

memory_api = {
    'mem_alloc':    'void* mem_alloc(void* size) {return NULL;} \n',
    'mem_addr':     'void mem_addr(void* addr, void* n, size_t length) {return;} \n',
    'mem_bytes':    'size_t* mem_bytes(void* ptr) {return -1;} \n',
    'mem_free':     'void summ_mem_free(void* ptr) {return;} \n',
}


sym_vars_api = {
    '_solver_Concat':   'symbolic _solver_Concat(symbolic sym_var, symbolic sym_var2, size_t length1, size_t length2) {return NULL;} \n', 
    '_solver_Extract':  'symbolic _solver_Extract(symbolic sym_var, size_t start, size_t end, size_t length) {return NULL;} \n',
    '_solver_ZeroExt':  'symbolic _solver_ZeroExt(symbolic sym_var, size_t to_extend, size_t length) {return NULL;} \n',
    '_solver_SignExt':  'symbolic _solver_SignExt(symbolic sym_var, size_t to_extend, size_t length) {return NULL;}\n'
}

constraints_api = {
    '_solver_NOT':      'cnstr_t _solver_NOT(cnstr_t cnstr1){return 0;} \n',
    '_solver_Or':       'cnstr_t _solver_Or(cnstr_t cnstr1, cnstr_t cnstr2) {return 0;} \n',
    '_solver_And':      'cnstr_t _solver_And(cnstr_t cnstr1, cnstr_t cnstr2) {return 0;} \n',
    '_solver_EQ':       'cnstr_t _solver_EQ(symbolic sym_var, symbolic sym_var2, size_t length) {return 0;} \n',
    '_solver_NEQ':      'cnstr_t _solver_NEQ(symbolic sym_var, symbolic sym_var2, size_t length) {return 0;} \n',
    '_solver_LT':       'cnstr_t _solver_LT(symbolic sym_var, symbolic sym_var2, size_t length) {return 0;} \n',
    '_solver_LE':       'cnstr_t _solver_LE(symbolic sym_var, symbolic sym_var2, size_t length) {return 0;} \n',
    '_solver_SLT':      'cnstr_t _solver_SLT(symbolic sym_var, symbolic sym_var2, size_t length) {return 0;} \n',
    '_solver_SLE':      'cnstr_t _solver_SLE(symbolic sym_var, symbolic sym_var2, size_t length) {return 0;} \n',
    '_solver_ITE':      'cnstr_t _solver_ITE(cnstr_t cond, cnstr_t cnstr1, cnstr_t cnstr2) {return 0;}\n',
    '_solver_ITE_VAR':  'cnstr_t _solver_ITE_VAR(cnstr_t cond, symbolic var1, symbolic var2, size_t len1, size_t len2) {return 0;}\n'
}

#Merge all 
all_api = {
    'new_sym_var':              'symbolic new_sym_var(size_t size) {return 0;}\n',
    'new_sym_var_named':        'symbolic new_sym_var_named(char* name, size_t size) {return 0;}\n',
    'new_sym_var_array':        'symbolic new_sym_var_array(char* name, size_t index, size_t size) {return 0;}\n',
    'save_current_state':       'state_t save_current_state() {return 0;} \n',
    'get_cnstr':                'cnstr_t get_cnstr(symbolic var, size_t size) {return 0;} \n',
    'store_cnstr':                 'void store_cnstr(char* name, cnstr_t constraint) {return;} \n',
    'halt_all':                 'void halt_all(state_t state) {return;} \n',
    'check_implications':       'result_t check_implications(char* constraint1, char* constraint2) {return 0;} \n',
    'print_counterexamples':    'void print_counterexamples(result_t result) {return;}\n',
    'error':                    'void error(char *fname) {return;} \n',
    'assume':                   'void assume(cnstr_t cnstr) {return;} \n',
    'is_symbolic':              'int is_symbolic(symbolic sym_var, size_t size) {return 0;} \n',
    'print_byte':               'void print_byte(char byte) {return;} \n',
    'maximize':                 'void* maximize(symbolic sym_var, size_t length) {return NULL;} \n',
    'is_sat':                   'int is_sat(cnstr_t cnstr) {return 0;}\n',
    'mem_alloc':                'void* mem_alloc(size_t size) {return NULL;} \n',
    'mem_addr':                 'mem_addr(void* addr, size_t length) \n',
    'mem_bytes':                'size_t mem_bytes(void* ptr) {return -1;} \n',
    'mem_free':                 'void summ_mem_free(void* ptr) {return;} \n',
    '_solver_Concat':           'symbolic _solver_Concat(symbolic sym_var, symbolic sym_var2, size_t length1, size_t length2) {return NULL;} \n', 
    '_solver_Extract':          'symbolic _solver_Extract(symbolic sym_var, size_t start, size_t end, size_t length) {return NULL;} \n',
    '_solver_ZeroExt':          'symbolic _solver_ZeroExt(symbolic sym_var, size_t to_extend, size_t length) {return NULL;} \n',
    '_solver_SignExt':          'symbolic _solver_SignExt(symbolic sym_var, size_t to_extend, size_t length) {return NULL;}\n',
    '_solver_NOT':              'cnstr_t _solver_NOT(cnstr_t cnstr1){return 0;} \n',
    '_solver_Or':               'cnstr_t _solver_Or(cnstr_t cnstr1, cnstr_t cnstr2) {return 0;} \n',
    '_solver_And':              'cnstr_t _solver_And(cnstr_t cnstr1, cnstr_t cnstr2) {return 0;} \n',
    '_solver_EQ':               'cnstr_t _solver_EQ(symbolic sym_var, symbolic sym_var2, size_t length) {return 0;} \n',
    '_solver_NEQ':              'cnstr_t _solver_NEQ(symbolic sym_var, symbolic sym_var2, size_t length) {return 0;} \n',
    '_solver_LT':               'cnstr_t _solver_LT(symbolic sym_var, symbolic sym_var2, size_t length) {return 0;} \n',
    '_solver_LE':               'cnstr_t _solver_LE(symbolic sym_var, symbolic sym_var2, size_t length) {return 0;} \n',
    '_solver_SLT':              'cnstr_t _solver_SLT(symbolic sym_var, symbolic sym_var2, size_t length) {return 0;} \n',
    '_solver_SLE':              'cnstr_t _solver_SLE(symbolic sym_var, symbolic sym_var2, size_t length) {return 0;} \n',
    '_solver_ITE':              'cnstr_t _solver_ITE(cnstr_t cond, cnstr_t cnstr1, cnstr_t cnstr2) {return 0;}\n',
    '_solver_ITE_VAR':          'cnstr_t _solver_ITE_VAR(cnstr_t cond, symbolic var1, symbolic var2, size_t len1, size_t len2) {return 0;}\n'
}


