# PySnapShot

This is a tiny helper package for saving code associated with
an experiment, and reloading it at a later time. There are two main functions:

1. `pysnapshot.capture`: Captures the code associated with a module into a snapshot at a given path.
2. `pysnapshot.load`: Loads the code from the snapshot into a module of a specified name. If no name is given, then the module name is whatever the folder
name is for the snapshot.

## Installation

Install from PyPI:

```bash
python -m pip install pysnapshot
```

## Usage

Let's say I'm working on the code in `examples/hello_world.py`. Let's save the current version 
(working in the `examples/` directory):

```python
import pysnapshot
import hello_world

# First let's take a snapshot of the 
# hello_world package.

path = pysnapshot.capture(hello_world, '/tmp/hello_world_snap/', overwrite=True)
hello_world_snap = pysnapshot.load(path)
print(hello_world_snap.__file__)

# The snapshot is loaded from the specified directory. The code was all copied to
# and is under the snapshot:

print("From original package code", hello_world.func1())
print("From snapshot", hello_world_snap.hello_world.func1())

# You can import from the snapshot as if it were a regular package

from hello_world_snap import hello_world
print("From snapshot, overwriting the original package code", hello_world.func1())
```

This has the output:

```bash
❯ cd examples/
❯ python demo.py
/private/tmp/hello_world_snap/__init__.py
/Users/prem/research/snapshot/examples/hello_world/hello.py TEST
From original package code TEST
/private/tmp/hello_world_snap/hello_world/hello.py TEST
From snapshot TEST
/private/tmp/hello_world_snap/hello_world/hello.py TEST
From snapshot, overwriting the original package code TEST
```

And it created a Python module with this directory structure:

```
❯ tree '/tmp/hello_world_snap/'
/tmp/hello_world_snap/
├── __init__.py
└── hello_world
    ├── __init__.py
    ├── hello.py
    └── nested
        └── __init__.py
```

## Releasing

Do the following steps:

```
python setup.py sdist
```

Upload it to test PyPI:

```
pip install twine
twine upload --repository testpypi dist/*
pip install -U --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple -U pysnapshot
```

Make sure you can install it and it works (e.g. run the examples). Now upload
to actual PyPI:

```
twine upload dist/*
```