"""
Main functionality of SnapShot is capturing and loading snapshots.
"""
import imp
from pathlib import Path
import os
import shutil
import re

IGNORE_PATTERNS = (
    '*.pyc',
    'tmp',
    '.git',
    '__pycache__'
)

def capture(module, snap_path, overwrite=False):
    """Captures a module into a snapshot directory. If the
    module already exists in the snapshot, an error is
    thrown unless overwrite=True. This creates a small
    "package" with the code required for the module 
    (discovered simply via looking up the parent directory
    of the module's __file__ attribute) copied as a submodule.

    Once captured, the code can be reloaded via the `load` 
    function. Multiple modules can be captured into one snapshot
    by calling this function on each module you want to capture.
    
    Parameters
    ----------
    module : ModuleType
        Module whose code that is being captured into a snapshot.
    snap_path : str
        Path to the saved snapshot module.
    overwrite : bool, optional
        If the module already exists in the snapshot, then an error
        will be thrown unless you choose to overwrite it., by default False

    Raises
    ------
    RuntimeError
        If overwrite is False and the module already exists in the snapshot, 
        an error is thrown.
    """
    src = Path(module.__file__).parent
    name = module.__name__
    dest = os.path.join(snap_path, name)

    if os.path.exists(dest):
        if overwrite:
            shutil.rmtree(dest)
        else:
            raise RuntimeError(f"Destination {dest} already exists.")
    
    shutil.copytree(
        src, dest, 
        ignore=shutil.ignore_patterns(*IGNORE_PATTERNS)
    )

    snap_init = Path(snap_path) / '__init__.py'
    if not os.path.exists(snap_init):
        snap_init.touch()
    
    _import_lines = [f"from . import {name}"]
    import_lines = []
    with open(snap_init, 'r') as f:
        existing_lines = f.readlines()
        for l in _import_lines:
            if l not in existing_lines:
                import_lines.append(l)

    with open(snap_init, 'a+') as f:
        f.writelines(import_lines)

    return snap_path

def load(snap_path, snap_name=None):
    """Loads a snapshot that was captured via the capture function. This
    returns an object that you can treat as if it were an imported module.

    Parameters
    ----------
    snap_path : str
        Path to the snapshot.

    Returns
    -------
    ModuleType
        Loaded module from snapshot, with submodules being the code
        you captured into this snapshot.
    """
    snap_path = Path(snap_path).resolve()
    snap_name = snap_name if snap_name is not None else snap_path.name

    fname, pname, desc = imp.find_module(str(snap_path))
    snap = imp.load_module(snap_name, fname, pname, desc)

    return snap
