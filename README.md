# ValidationGen

## Installation

```bash
$ ./install.sh
```

### To uninstall run:

```bash
$ ./install.sh -u
```

# Usage

## Generate a simple test for ``strlen`` 

Given a concrete function for ``strlen`` and a corresponding summary (files ``summ_strlen.c`` and ``concrete_strlen.c``) one can generate a simple validation using:

```sh
$ summvalgen -summ summ_strlen.c -func concrete_strlen.c
```

By default this will generate a file called `test.c` containing the symbolic test where `strlen` is called with a symbolic string of **size 5**. Additionally, instead of the default value **5**, the length of the symbolic string used as input argument can be specified using the `--arraysize` flag:

```sh
$ summvalgen -summ summ_strlen.c -func concrete_strlen.c --arraysize=3
```

In order to execute the generated tests in a symbolic exeuction tool, a binary file is usually required. To this end, one can pass the `--compile` flag:

```sh
$ summvalgen -summ summ_strlen.c -func concrete_strlen.c -compile
```

This automatically compiles the generated test to an *x86* binary. Alternatively, the target *arch* can be specified. For instance, the command:

```sh
$ summvalgen -summ summ_strlen.c -func concrete_strlen.c -compile=x64
```
compiles the test to *x84_64* architecture.

