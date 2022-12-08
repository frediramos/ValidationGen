
char* summ_strcpy(char* dest, char* source){
	int i = 0;
	char zero = '\0';

	while(1){
		if(is_symbolic(&source[i],8)){
			
			if(!is_sat(_solver_NEQ(&source[i], &zero, 8))){
				break;
			}
			
			else{
				assume(_solver_NEQ(&source[i], &zero, 8));
			}
		}

		else if(source[i] == '\0'){
			break;
		}
		dest[i] = source[i];
		i++;
	}

	dest[i] = '\0';
	return dest;

}