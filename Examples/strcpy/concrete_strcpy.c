//Concrete implementation to be compared with
char* concrete_strcpy(char* dest, char* source){
	char* save = dest;
	while (*source){
	   *dest++ = *source++;
	}
	*dest = '\0';
	return (char *) save;
}
