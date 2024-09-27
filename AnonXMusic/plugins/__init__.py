import os
from glob import glob
from os.path import join, basename, dirname, isfile

async def all_plugins():
    # This generates a list of plugins in this folder for the * in __main__ to work.

    work_dir = dirname(__file__)
    mod_paths = glob(join(work_dir, "**/*.py"), recursive=True)
    all_plugs = [
        ((f.replace(work_dir, "")).replace("/", ".").replace("\\", ".")[1:-3])
        for f in mod_paths
        if isfile(f) and f.endswith(".py") and not f.endswith("__init__.py")
    ]
    return sorted(all_plugs)