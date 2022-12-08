
//Summary implementation to be compared with
size_t summ_strlen(char* s){
	int i = 0;
	char zero = '\0';

	while(1){
		if(is_symbolic(&s[i],8)){
			
			if(!is_sat(_solver_NEQ(&s[i], &zero, 8))){
				break;				
			}
			
			else{
				
				symbolic val = new_sym_var_named("a", 32);
				cnstr_t r = _solver_NOT(_solver_SLT(&val, &i, 32));
				assume(r);

				return val;
			}
		}
		else if(s[i] == '\0'){
			break;
		}
		
		i++;
	}

	return i;
}