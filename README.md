![build status](https://travis-ci.org/OhadRubin/awesome-system-design.svg?branch=master)
![coverage](https://codecov.io/gh/OhadRubin/awesome-system-design/branch/master/graph/badge.svg)

# Awesome System Design

An example package. See [full documentation](https://advanced-system-design-awesome-system-design.readthedocs.io/en/latest/).

## Installation

1. Clone the repository and enter it:

    ```sh
    $ git clone git@github.com:OhadRubin/awesome-system-design.git
    ...
    $ cd awesome-system-design/
    ```

2. Run the installation script and activate the virtual environment:

    ```sh
    $ ./scripts/install.sh
    ...
    $ source .env/bin/activate
    [awesome-system-design] $ # you're good to go!
    ```

3. To check that everything is working as expected, run the tests:


    ```sh
    $ pytest tests/
    ...
    ```

## Usage

The `asd` packages provides the following classes:

- `Foo`

    This class encapsulates the concept of `foo`, and returns `"foo"` when run.

    In addition, it provides the `inc` method to increment integers, and the
    `add` method to sum them.

    ```pycon
    >>> from asd import Foo
    >>> foo = Foo()
    >>> foo.run()
    'foo'
    >>> foo.inc(1)
    2
    >>> foo.add(1, 2)
    3
    ```

- `Bar`

    This class encapsulates the concept of `bar`; it's very similar to `Foo`,
    except it returns `"bar"` when run.

    ```pycon
    >>> from asd import Bar
    >>> bar = Bar()
    >>> bar.run()
    'bar'
    ```

The `asd` package also provides a command-line interface:

```sh
$ python -m asd
asd, version 0.1.0
```

All commands accept the `-q` or `--quiet` flag to suppress output, and the `-t`
or `--traceback` flag to show the full traceback when an exception is raised
(by default, only the error message is printed, and the program exits with a
non-zero code).

The CLI provides the `foo` command, with the `run`, `add` and `inc`
subcommands:

```sh
$ python -m asd foo run
foo
$ python -m asd foo inc 1
2
$ python -m asd foo add 1 2
3
```

The CLI further provides the `bar` command, with the `run` and `error`
subcommands.

Curiously enough, `bar`'s `run` subcommand accepts the `-o` or `--output`
option to write its output to a file rather than the standard output, and the
`-u` or `--uppercase` option to do so in uppercase letters.

```sh
$ python -m asd bar run
bar
$ python -m asd bar run -u
BAR
$ python -m asd bar run -o output.txt
$ cat output.txt
BAR
```

Do note that each command's options should be passed to *that* command, so for
example the `-q` and `-t` options should be passed to `asd`, not `foo` or
`bar`.

```sh
$ python -m asd bar run -q # this doesn't work
ERROR: no such option: -q
$ python -m asd -q bar run # this does work
```

To showcase these options, consider `bar`'s `error` subcommand, which raises an
exception:

```sh
$ python -m asd bar error
ERROR: something went terribly wrong :[
$ python -m asd -q bar error # suppress output
$ python -m asd -t bar error # show full traceback
ERROR: something went terribly wrong :[
Traceback (most recent call last):
    ...
RuntimeError: something went terrible wrong :[
```
