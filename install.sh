#!/bin/bash

SYMDIR=/usr/local/bin
SUMMBV_PY=SummBoundVerify.py
SUMMBV=summbv
ANGR_VERSION=9.2.6
VIRTUALENV_NAME=angr


# $1: file path
# $2: sym link directory
# $3: sym link name
make_symLink () {
	link=$2/$3
	sudo ln -sf $1 $link
	if [ -L $link ] && [ -e $link ]; then
		echo "sym link created: $3 -> $1"
		return 0
	else
		return 1
	fi
}


install_pycparser () {
	apt-get -y install python3-dev python3-pip libffi-dev build-essential
	if python3 -m pip install Pycparser==2.21; then
		return 0
	else
		return 1
	fi
}


install_mkvirtualenv () {
	if python3 -m pip install virtualenv virtualenvwrapper; then	
		workon_home=$HOME/.virtualenvs
		mkdir -p $workon_home
		
		echo "export WORKON_HOME=$workon_home" >> ~/.bashrc
		echo "export VIRTUALENVWRAPPER_PYTHON=$(which python3)" >> ~/.bashrc
		echo "source $(which virtualenvwrapper.sh)" >> ~/.bashrc
		
		export VIRTUALENVWRAPPER_PYTHON=$(which python3)
		source $(which virtualenvwrapper.sh)
		if [ -x "$(command -v mkvirtualenv)" ] && [ -x "$(command -v workon)" ] ; then
			return 0
		fi
	fi
	return 1
}


install_angr_package () {
	command="python3 -m pip install angr==${ANGR_VERSION}"
	if $1 ; then
		export VIRTUALENVWRAPPER_PYTHON=$(which python3)
		source $(which virtualenvwrapper.sh)
		command="mkvirtualenv --python=$(which python3) ${VIRTUALENV_NAME} && ${command}"
	fi
	if eval $command; then
		return 0
	else
		return 1
	fi
}

install_angr () {

	# Virtualenvwrapper ----------------------------------------------------------------------------------
	source $(which virtualenvwrapper.sh)	
	if command -v mkvirtualenv &> /dev/null ; then
		echo Virtualenvwrapper already installed, continuing
		virtualenv=true
	else
		echo "=> Installing Virtualenvwrapper"
		if ! install_mkvirtualenv; then
			echo Could not install Virtualenvwrapper
			while true; do
				read -p "Do you wish to install 'angr' in the current Python env ($(which python3))? (yn)  " yn
				case $yn in
					[Yy]* ) 
						virtualenv=false;
						break;;
					[Nn]* ) 
						echo "SummBoundVerify can still be used for test genration...";
						angr=false
						return 1;;
					* ) echo "Please answer (y)es or (n)o.";;
				esac
			done
		fi
	fi

	# angr -----------------------------------------------------------------------------------------------
	echo
	echo "=> Installing angr"
	if install_angr_package $virtualenv; then
		echo "angr installed successfully"
		return 0
	else
		angr=false
		echo Could not install angr
		return 1
	fi
}


install () {

	# Pycparser ------------------------------------------------------------------------------------------
	echo "=> Installing Pycparser"
	if install_pycparser; then
		echo "Pycparser installed successfully"
	else
		echo "Could not install crucial Python dependency: Pycparser V2.21"
		exit 1
	fi

	# Install angr? --------------------------------------------------------------------------------------
	while true; do
		read -p "Do you wish to install 'angr'? This is required to run validation tests (yn)  " yn
		case $yn in
			[Yy]* ) 
				angr=true;
				install_angr
				break;;
			[Nn]* ) 
				angr=false;
				break;;
			* ) echo "Please answer (y)es or (n)o.";;
		esac
	done

	
	# Final symlinks -------------------------------------------------------------------------------------------
	echo
	echo "=> Installing 'SummBoundVerify'"
	if make_symLink $(pwd)/$SUMMBV_PY $SYMDIR $SUMMBV; then
		echo
		if $angr; then
			echo "* SummBoundVerify installed sucessfully! *"
			echo "Use ./~.bashrc to reload current shell" 

			if $virtualenv; then
				echo
				echo "Activate angr's virtualenv before running a validation test: workon $VIRTUALENV_NAME" 
			fi

		else
				echo "angr was not installed"
				echo "But SummBoundVerify can still be used for symbolic test generation"
			fi
		fi
	
	else
		echo
		echo "Could not create a symLink for $SUMMBV_PY in $SYMDIR"
		echo "Try running with root access: 'sudo ./install -l' "
		echo "Or create it mannually: sudo ln -sf $SUMMBV_PY <directory_in_PATH> "
	fi
	
	# Complete
	echo
	echo
	echo "To uninstall run './install -u'"
	return 0
	# ----------------------------------------------------------------------------------------------------

}

uninstall () {
	
	link=$SYMDIR/$SUMMBV
	if [ -L $link ] && [ -e $link ]; then
		sudo unlink -f $link
	fi
	echo SummBoundVerify Removed
	return  $status	
}


display_help () {
	echo "** SummBoundVerify install script **"
	echo
	echo "Use ./install for complete installation"
	echo
	echo "Flag Options:"
	echo "-u: Uninstall SummBoundVerify"
	echo "-l: Create symbolic link 'summbv' in PATH and exit"
	echo "-h: Display this message and exit"
}


if [[ $# -eq 0 ]] ; then
	install || exit 1
else
	case "$1" in
		-u) echo "=> Uninstalling SummValidationGen"
			uninstall;
			exit 0;;
		-l)
			make_symLink $(pwd)/$SUMMBV_PY $SYMDIR $SUMMBV
			exit 0;;

		-h)
			display_help;
			exit 0;;
		* ) 
			echo "Unknown option: Use ./install -h for help.";
			exit 0;;
	esac
fi