import sys
import pysnapshot as snapshot
import imp
import importlib
from pathlib import Path
import tempfile
import shutil
import pytest

def _load_module_from_path(module_name, path):
    fname, pname, desc = imp.find_module(path)
    module = imp.load_module(module_name, fname, pname, desc)
    return module

def test_hello_world_defaults():
    path = str(Path('examples/hello_world').resolve())
    hello_world = _load_module_from_path('hello_world', path)
    func1_val = hello_world.func1()
    nested_val = hello_world.nested.nested_func1()

    with tempfile.TemporaryDirectory() as tmpdir:
        snapshot.capture(hello_world, tmpdir, overwrite=True)
        snap = snapshot.load(tmpdir, "snap")
        assert tmpdir in str(Path(snap.__file__).parent)

        assert snap.hello_world.func1() == func1_val
        assert snap.hello_world.nested.nested_func1() == nested_val

        from snap import hello_world as snap_hello_world

        assert snap_hello_world.func1() == func1_val
        assert snap_hello_world.nested.nested_func1() == nested_val

        pytest.raises(RuntimeError, snapshot.capture, 
            hello_world, tmpdir, overwrite=False)

def test_hello_world_with_modification():
    path = str(Path('examples/hello_world').resolve())

    with tempfile.TemporaryDirectory() as moddir:
        moddir = '/tmp/snapshot/'
        shutil.rmtree(moddir)
        moddir = Path(moddir)
        shutil.copytree(path, moddir / 'hello_world_copy')
        
        # Modify it
        with open(moddir / 'hello_world_copy' / 'hello.py', 'r') as f:
            lines = f.readlines()
            new_lines = []
            for l in lines:
                if 'TEST' in l:
                    l = l.replace('TEST', 'MODIFIED')
                new_lines.append(l)
        
        with open(moddir / 'hello_world_copy' / 'hello.py', 'w') as f:
            f.writelines(new_lines)

        # Load modified package and snapshot it
        hello_world_copy = _load_module_from_path('hello_world_copy', str(moddir / 'hello_world_copy'))
        func1_val = hello_world_copy.func1()
        nested_val = hello_world_copy.nested.nested_func1()
        assert func1_val == 'MODIFIED'

        with tempfile.TemporaryDirectory() as tmpdir:
            snapshot.capture(hello_world_copy, tmpdir, overwrite=True)
            snap_copy = snapshot.load(tmpdir, "snap_copy")
            assert tmpdir in str(Path(snap_copy.__file__).parent)

            assert snap_copy.hello_world_copy.func1() == func1_val
            assert snap_copy.hello_world_copy.nested.nested_func1() == nested_val

            from snap_copy import hello_world_copy as snap_hello_world

            assert snap_hello_world.func1() == func1_val
            assert snap_hello_world.nested.nested_func1() == nested_val

