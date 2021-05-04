#!./venv/bin/python
# %%

import numpy.f2py
import os
import subprocess
import json
from warnings import warn

BUILD_DIR = 'build_f2py'
os.makedirs(BUILD_DIR, exist_ok=True)

# %%
# Find fortran compile map files
compile_map_files = [[dr, f]for dr, d, flist in os.walk('./src')
                     if os.path.isdir(dr) for f in flist if f == "compile_map.json"]
compile_map_files
# %%
# %%
for (dir, compile_map) in compile_map_files:
    with open(f"{dir}/{compile_map}") as compile_map_r:
        compile_info = json.load(compile_map_r)
        mod_name = compile_info['mod_name']
        print(f'Compiling {mod_name}')

        # Compile Libraries
        libraries = [f"{dir}/{lib}" for lib in compile_info['libraries']]
        with subprocess.Popen(['gfortran', '-J', BUILD_DIR, '-c'] + libraries, stdout=subprocess.PIPE, stderr=subprocess.PIPE) as p:
            p.wait()
            if p.returncode != 0:
                warn(f"{dir} - {mod_name} failed {p.stderr.read().decode('utf-8')}")
                break
            # TODO: Move libraries back to src dir

        # Compile main files
        py_interface_files = [
            f"{dir}/{lib}" for lib in compile_info['py_interface_files']]
        with subprocess.Popen(['f2py', '-c', '--build-dir', BUILD_DIR, '-m', mod_name] + py_interface_files, stdout=subprocess.PIPE, stderr=subprocess.PIPE) as p:
            # print(p.stdout.read().decode('utf-8'))
            p.wait()
            if p.returncode != 0:
                warn(f"{dir} - {mod_name} failed {p.stderr.read().decode('utf-8')}")

        # Cleanup build files

# %%
with subprocess.Popen(['f2py', '-c', '-m', 'ewert', 'src/ewert.f90'], stdout=subprocess.PIPE) as p:
    # stdout, stderr = p.communicate()
    print(p)
    print(p.stdout.read().decode('utf-8'))
