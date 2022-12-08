int summ_toupper(int c){

	if (is_symbolic(&c, 32)){

		symbolic ret = new_sym_var_named("ret", 32);
		
		int l_bound = 97;
		int u_bound = 122;

		cnstr_t c_geq = _solver_NOT(_solver_SLT(&c, &l_bound, 32));
		cnstr_t c_leq = _solver_SLE(&c, &u_bound, 32);
		
		symbolic lower_c = c - 32;
		
        cnstr_t lower_cnstr = _solver_EQ(&ret, &lower_c, 32);
		cnstr_t unchanged_cnstr = _solver_EQ(&ret, &c, 32);

		cnstr_t final_cnstr = _solver_ITE(_solver_And(c_geq, c_leq), lower_cnstr, unchanged_cnstr);
		assume(final_cnstr);

		return ret;
	}

	else{

		if (c >= 65 && c <= 90){
			return c - 32;
		}
		return c;
		
	}
}
