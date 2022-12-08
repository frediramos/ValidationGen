void* summ_memcpy(void *dest, void *src, size_t n){

	//If length is symbolic maximizes to a concrete length
	if(is_symbolic(&n,32)){

		n = maximize(&n,32);
	}
	
	unsigned char *str_dest = (unsigned char*) dest;
	unsigned char *str_src = (unsigned char*) src;

	for(int i = 0; i < n; i++){

		unsigned char c = *(str_src + i);
		*(str_dest + i) = c;

	}
	return dest;
}