# ValidationGen

## Installation

```bash
$ ./install.sh
```

### To uninstall run:

```bash
$ ./install.sh -u
```

# Basic Usage
To obtain a full description of our test generatiom tool one can use the flag `-h`
```
$ summvalgen -h
```

## Generate a simple test for ``strlen`` 

Given a concrete function for ``strlen`` and a corresponding summary (files ``summ_strlen.c`` and ``concrete_strlen.c``) one can generate a simple validation test using:

```sh
$ summvalgen -summ summ_strlen.c -func concrete_strlen.c
```

By default this will generate a file called `test.c` containing the symbolic test where `strlen` is called with a symbolic string of **size 5**. Additionally, instead of the default value **5**, the length of the symbolic string used as input argument can be specified using the `--arraysize` flag:

```sh
$ summvalgen -summ summ_strlen.c -func concrete_strlen.c --arraysize=3
```

## Generate multiple tests
To generate a single test file containing multiple executions for  different arrays sizes one can also pass an array of values to the `--arraysize` flag:

```sh
$ summvalgen -summ summ_strlen.c -func concrete_strlen.c --arraysize 3 5 7 -compile
```


## Compile to a binary
In order to execute the generated tests in a symbolic exeuction tool, a binary file is usually required. To this end, one can pass the `--compile` flag:

```sh
$ summvalgen -summ summ_strlen.c -func concrete_strlen.c -compile
```

This automatically compiles the generated test to an *x86* binary. Alternatively, the target *arch* can be specified. For instance, the command:

```sh
$ summvalgen -summ summ_strlen.c -func concrete_strlen.c -compile=x64
```
compiles the test to *x84_64* architecture.

## Function names and Libraries

To evaluate a tool summary (not implemented in a separate file) one can simply specify its name using the ``--summ_name`` flag: 

```sh
$ summvalgen -summ_name strlen -func concrete_strlen.c -compile=x64
```

Additionally, it is often the case that a summary or concrete function may not be self contained in a single C file. To this end, when compiling a test using the `--compile` flag one can also pass additional files with the ``--lib`` flag:

```sh
$ summvalgen -summ summ_strlen.c -func concrete_strlen.c -compile --lib lib1.c lib2.c 
```


## Constrain numeric values

For some ``libc`` functions, using fully symbolic arguments can lead to unbound loops in the concrete functions. To constrain numeric values one can use the ``--maxvalue`` flag. For instance considering a test for the ``memcpy(void *dest, const void *src, size_t len)`` function, the command:

```sh
$ summvalgen -summ summ_memcpy.c -func concrete_memcpy.c -maxvalue=5
```

will generate a test where the ``len`` argument is constrained to be lower or equal than ``5``.

## Evaluate memory functions
By default the summary validation tool only takes into account the generated paths and corresponding return values. Hence, in order to evaluate a summary for a function with memory side-effects such ``memcpy``, one can use the ``-memory`` flag:

```sh
$ summvalgen -summ summ_memcpy.c -func concrete_memcpy.c -maxvalue=5 -memory
```
This flag marks the relevant memory addresses in the summary's execution so that they are also be evaluated.

# Configuration Files

In alternative to the command line interface, one can also pass a configuration file using the ``-config`` flag. For instance, considering the configuration file (``config.txt``): 

```
array_size 3 5 7
func_file concrete_strlen.c
summ_file summ_strlen.c
compile_arch x86
```

The command:
```sh
$ summvalgen -config config.txt
```
is equivalent to:
```sh
$ summvalgen -summ summ_strlen.c -func concrete_strlen.c --arraysize 3 5 7 -compile
```

## All Config file options

The options allowed in the configuration file mirror some of the flags offered in the command line interface:

```
func_file  concrete.c       // -func
summ_file  summ.c           // -summ
summ_name  strlen           // --summ_name
func_name  summ_strlen      // --func_name
array_size 5                // --arraysize
null_bytes 3                // --nullbytes
default_values {1:'NULL'}   // --defaultvalues
max_num                     // --maxvalue
max_names len               // --maxnames
concrete_array {1:[0]}      // --concretearray
lib lib.c                   // --lib
compile_arch x86            // --compile
```