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
To generate a single test file containing multiple executions for  different arrays sizes one can pass an array of values to the `--arraysize` flag:

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


## Constrain numeric values

For some ``libc`` functions, using fully symbolic arguments can lead to unbound loops in the concrete functions. To constrain numeric values one can use the ``--maxvalue`` flag. For instance considering a test for the ``memcpy(void *dest, const void *src, size_t len)`` function, the command:

```sh
$ summvalgen -summ summ_memcpy.c -func concrete_memcpy.c -maxvalue=5
```

will generate a test where the ``len`` argument is constrained to be lower or equal than ``5``.

## Evaluate memory functions
By default the summary validation tool only takes into account the generated paths and corresponding return valuel. Hence, in order to evaluate a summary for a function with memory side-effects such ``memcpy``, one can use the ``-memory`` flag:

```sh
$ summvalgen -summ summ_memcpy.c -func concrete_memcpy.c -maxvalue=5 -memory
```
This flag marks the relevant memory addresses in the summary's execution to be evaluated.