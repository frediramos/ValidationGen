SHELL:=/bin/bash

TEST = $(shell basename $(CURDIR))_validation.c
EXEC = $(shell basename $(CURDIR))_validation.test
SUMM = $(shell basename $(CURDIR)).c
RESULT = $(EXEC)_result.json

EXPECTED_TEST = expected_test.c
EXPECTED_RSLT = expected_result.json

CONFIG = config.txt

.PHONY: gen run test clean

gen:
	summbv -config $(CONFIG) -o $(TEST) -memory

run:
	summbv -config $(CONFIG) -o $(TEST) -memory -run
	
test:
	summbv -config $(CONFIG) -o $(TEST) -memory
	
	@diff -Bb $(TEST) $(EXPECTED_TEST);\
	if [ $$? -eq 0 ]; \
	then \
		echo -e "\nTest Passed!"; \
	else \
		echo -e "\nTest Failed!"; \
	fi

test-run:

	summbv -config $(CONFIG) -o $(TEST) -memory -run
	@diff -Bb  <(sed '3q;d' $(EXPECTED_RSLT)) <(sed '3q;d' $(RESULT));\
	if [ $$? -eq 0 ]; \
	then \
		echo -e "\nTest Passed!"; \
	else \
		echo -e "\nTest Failed!"; \
	fi

clean:
	$(RM) *.o *.test $(TEST) $(EXEC) $(RESULT)