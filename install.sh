#!/bin/bash

FILE=summ_val_gen.py
SYMLINK=summvalgen
SYMDIR=/usr/local/bin

if [[ $# -eq 0 ]] ; then
	echo "=> Intalling Pycparser"

	if python3 -m pip install Pycparser==2.21; then
		echo Pycparser installed successfully
	else
		echo Could not install required Python dependency: Pycparser V2.21
		exit 1
	fi

	echo
	echo "=> Intalling SummValidationGen"
	sudo ln -sf $(pwd)/$FILE $SYMDIR/$SYMLINK
	
	if test $SYMLINK; then
		echo SummValidation installed successfully
		echo Use $SYMLINK -h for help
	else
		echo Could not create symLink for $FILE in $SYMDIR
		exit 1
	fi
	echo "Use ./install -u to uninstall"
	exit 0
fi


case "$1" in
	-u) echo "=> Uninstalling SummValidationGen"
	
		if [ -L $SYMDIR/$SYMLINK ]; then
			sudo unlink -f $SYMDIR/$SYMLINK
			STATUS=0
		else 
			STATUS=1
		fi
		echo SummValidationGen Removed
		exit $STATUS	
esac