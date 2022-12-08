void* summ_memcpy(void *dest, void *src, size_t n){

	//If length is symbolic maximize and cnstrict to a concrete length
	if(is_symbolic(&n,32)){

		size_t max = maximize(&n, 32);
		cnstr_t maximize = _solver_EQ(&n, &max, 32);
		assume(maximize);
		n = max;
	}
	
	unsigned char *str_dest = (unsigned char*) dest;
	unsigned char *str_src = (unsigned char*) src;

	for(int i = 0; i < n; i++){

		unsigned char c = *(str_src + i);
		*(str_dest + i) = c;

	}
	return dest;
}