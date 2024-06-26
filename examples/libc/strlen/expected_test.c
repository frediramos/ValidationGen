/*File generated by 'summvalgen'*/

#define NULL ((void*)0)
#define INT_SIZE (sizeof(int) * 8)
#define LONG_SIZE (sizeof(long) * 8)
#define CHAR_SIZE (sizeof(char) * 8)
#define PTR_SIZE (sizeof(void*) * 8)
typedef void* symbolic;
typedef int state_t;
typedef unsigned int size_t;
typedef unsigned int cnstr_t;
typedef unsigned int result_t;

cnstr_t _ULE_(symbolic var1, symbolic var2) {return 0;}
cnstr_t get_cnstr(symbolic var, size_t size) {return 0;}
result_t check_implications(char* constraint1, char* constraint2) {return 0;}
state_t save_current_state() {return 0;}
symbolic sym_var_array(char* name, size_t index, size_t size) {return 0;}
symbolic sym_var_named(char* name, size_t size) {return 0;}
void assume(cnstr_t cnstr) {return;}
void halt_all(state_t state) {return;}
void mem_addr(char* name, void* addr, size_t length) {return;}
void print_counterexamples(result_t result) {return;}
void store_cnstr(char* name, cnstr_t constraint) {return;}

cnstr_t _AND_(cnstr_t cnstr1, cnstr_t cnstr2) {return 0;}
cnstr_t _EQ_(symbolic var1, symbolic var2) {return 0;}
cnstr_t _GE_(symbolic var1, symbolic var2) {return 0;}
cnstr_t _GT_(symbolic var1, symbolic var2) {return 0;}
cnstr_t _ITE_(cnstr_t cnstr1, cnstr_t cnstr2, cnstr_t cnstr3) {return 0;}
cnstr_t _ITE_VAR_(cnstr_t cnstr1, symbolic var1, symbolic var2) {return 0;}
cnstr_t _LE_(symbolic var1, symbolic var2) {return 0;}
cnstr_t _LT_(symbolic var1, symbolic var2) {return 0;}
cnstr_t _NEQ_(symbolic var1, symbolic var2) {return 0;}
cnstr_t _NOT_(cnstr_t cnstr) {return 0;}
cnstr_t _OR_(cnstr_t cnstr1, cnstr_t cnstr2) {return 0;}
cnstr_t _UGE_(symbolic var1, symbolic var2) {return 0;}
cnstr_t _UGT_(symbolic var1, symbolic var2) {return 0;}
cnstr_t _ULT_(symbolic var1, symbolic var2) {return 0;}
void _assert(int expr){return;}
int is_certain(cnstr_t cnstr){return 0;}
int is_sat(cnstr_t cnstr); 
int is_symbolic(symbolic sym_var) {return 0;} 
long maximize(symbolic sym_var){return 0;}
void pop_pc(){return;}
void push_pc(){return;}
symbolic sym_var(size_t size) {return 0;}

#define POINTER_SIZE 5
#define FUEL 5
#define ARRAY_SIZE_1 3


size_t concrete_strlen(const char *str)
{
  size_t i;
  for (i = 0;; i++)
    if (str[i] == 0)
    return i;

}

void test_1()
{
  char str[ARRAY_SIZE_1];
  for (int str_idx_1 = 0; str_idx_1 < ARRAY_SIZE_1; str_idx_1++)
  {
    str[str_idx_1] = sym_var_array("str", str_idx_1, sizeof(char) * 8);
  }

  str[ARRAY_SIZE_1 - 1] = '\0';
  state_t initial_state = save_current_state();
  size_t ret1 = concrete_strlen(str);
  cnstr_t cnstr1 = get_cnstr(&ret1, sizeof(size_t) * 8);
  store_cnstr("cnctr_test1", cnstr1);
  halt_all(initial_state);
  size_t ret2 = strlen(str);
  cnstr_t cnstr2 = get_cnstr(&ret2, sizeof(size_t) * 8);
  store_cnstr("summ_test1", cnstr2);
  halt_all(NULL);
  result_t result = check_implications("cnctr_test1", "summ_test1");
  print_counterexamples(result);
  return ;
}

int main()
{
  test_1();
}