//Summary implementation to be compared with

size_t summ_strlen(char* s){
 	
 	int i = 0;
 	char char_zero = '\0';

 	//Calculate max string length
 	while(is_symbolic(&s[i],CHAR_SIZE) || s[i] != '\0'){
		i++;
 	}

	int len = i;
	symbolic ret = new_sym_var(INT_SIZE);
	cnstr_t ret_cnstr = _solver_EQ(&ret, &len, INT_SIZE);

	//Build recursive ITE constraint
	for(i = len-1; i >= 0; i--){

		if(is_symbolic(&s[i],CHAR_SIZE)){

			cnstr_t c_eq_zero = _solver_EQ(&s[i], &char_zero, CHAR_SIZE);
			cnstr_t ret_eq_i = _solver_EQ(&ret, &i, INT_SIZE);

			ret_cnstr = _solver_ITE(c_eq_zero, ret_eq_i, ret_cnstr);
			
		}
	}

	assume(ret_cnstr);
	return ret;
}