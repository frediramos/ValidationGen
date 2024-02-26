TEST = $(shell basename $(CURDIR))_validation.c
EXEC = $(shell basename $(CURDIR))_validation.test
SUMM = $(shell basename $(CURDIR)).c
CONFIG = config.txt

.PHONY: all clean

all:
	summbv -config $(CONFIG) -o $(TEST)
# run:
# 	summbv -config $(CONFIG) -o $(TEST) --lib $(SUMM)

clean:
	$(RM) *.o *.test $(TEST) *.json