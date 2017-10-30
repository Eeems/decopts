# Installation
```
pip install decparse
```

# Usage

Before with argeparse
```python
import argparse

parser = argparse.ArgumentParser(
    prog='foo',
    description='Print bar',
    add_help=True
)
parser.add_argument(
    '--baz',
    action='store_true'
    help='Also print baz'
)
args = parser.parse_arguments()

print('bar')
if args.baz:
    print('baz')
```
Using decopts instead
```python
from decopts import entrypoint, option

@entrypoint(
    prog='foo',
    description='Print bar',
    add_help=True
)
@option(
    '--baz',
    action='store_true'
    help='Also print baz'
)
def main():
    print('bar')
    if main.args.baz:
        print('baz')

main()
```
Adding subcommands
```python
from decopts import entrypoint, option, action

@entrypoint(
    prog='foo',
    description='Print something',
    add_help=True
)
def main():
    return

@action(
    main,
    'foo',
    description='Print foo'
)
def foo():
    print('foo')

@action(
    main,
    'baz',
    description='Print baz'
)
def baz():
    print('baz')

main()

```
