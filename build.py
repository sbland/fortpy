#! ./venv/bin/python
"""Build all Fortran modules.


The aim is to have isolated modules that contain both fortran and python code.
Each module should be able to compile and run tests in isolation.

This file scans each module for fortran files and builds the module.

# TODO: What is the best way of flagging a directory for fortan compiling
# TODO: What is the best way of identifying which files are python interfaces

"""
import click
import sys
import shutil
import os
from warnings import warn
import subprocess

BUILD_DIR_NAME = "_build_dir"
CC = "gcc"
F90 = "gfortran"
PYTHON = "python"

FPP = ["gfortran", "-E"]
FPP_F90FLAGS = ["-x", "f95-cpp-input", "-fPIC"]
F90FLAGS = ["-fPIC"]
FCOMP = "gfortran"
LIBS = ""

CFLAGS = ["-dPIC"]

# UNAME = "$(shell uname)"

LIBTOOL = ["ar", "src"]


# ======================================================================
# PROJECT CONFIG, do not put spaced behind the variables
# ======================================================================
# mapping between Fortran and C types
KIND_MAP = "kind_map"


# =======================================================================
#       List all source files required for the project
# =======================================================================


# names (without suffix), f90 sources
LIBSRC_SOURCES = ["config", "external_state", "model_state", "pipeline"]

# file names
LIBSRC_FILES = [f"{f}.f90" for f in LIBSRC_SOURCES]

# object files
LIBSRC_OBJECTS = [f"{f}.o" for f in LIBSRC_SOURCES]

# only used when cleaning up
LIBSRC_FPP_FILES = [f"{f}.fpp" for f in LIBSRC_SOURCES]


# =======================================================================
#       List all source files that require a Python interface
# =======================================================================

# names (without suffix), f90 sources
LIBSRC_WRAP_SOURCES = ["config", "external_state", "model_state", "pipeline"]

# file names
LIBSRC_WRAP_FILES = [f"{f}.f90" for f in LIBSRC_WRAP_SOURCES]

# object files
LIBSRC_WRAP_OBJECTS = [f"{f}.o" for f in LIBSRC_WRAP_SOURCES]

# only used when cleaning up
LIBSRC_WRAP_FPP_FILES = [f"{f}.fpp" for f in LIBSRC_WRAP_SOURCES]


# =======================================================================
#                 Relevant suffixes
# =======================================================================

SUFFIXES = [".f90", ".fpp"]


# =======================================================================
#                 Functions
# =======================================================================

SRC_DIR = "./"


def run_subprocess(cmd, cwd=".", strict=True):
    try:
        print("cmd: [" + " ".join(cmd) + "]")
    except TypeError as e:
        print(cmd)
    with subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=cwd) as p:
        p.wait()
        if p.returncode != 0:
            warn(f"cmd: [" + " ".join(cmd) +
                 "] failed {p.stderr.read().decode('utf-8')}")
            if strict:
                raise Exception("Process Failed")


def libsrc_a_files(mod_path, build_dir):
    print("====== Building libsrc files =====")
    f90_0_files(mod_path, build_dir)
    cmd = LIBTOOL + ["libsrc.a"] + LIBSRC_OBJECTS
    run_subprocess(cmd, cwd=build_dir)
    # ${LIBTOOL} $@ $?


def f90_fpp_files(mod_path, build_dir):
    print("====== Building fpp files =====")
    for (fin, fout) in zip(LIBSRC_FILES, LIBSRC_FPP_FILES):
        cmd = FPP + FPP_F90FLAGS + \
            [f"-J{BUILD_DIR_NAME}"] + [fin] + ["-o"] + [fout]
        run_subprocess(cmd, cwd=mod_path)
        shutil.move(f"{mod_path}/{fout}", f"{build_dir}/{fout}")
        # ${FPP} ${FPP_F90FLAGS} $<  -o $@
    print("====== ================ =====")


def f90_0_files(mod_path, build_dir):
    print("====== Building o files =====")
    for f, o in zip(LIBSRC_FILES, LIBSRC_OBJECTS):
        cmd = [F90] + F90FLAGS + \
            [f"-J{BUILD_DIR_NAME}"] + ["-c"] + [f] + ["-o"] + [o]
        run_subprocess(cmd, cwd=mod_path)
        shutil.move(f"{mod_path}/{o}", f"{build_dir}/{o}")
    # ${F90} ${F90FLAGS} -c $< -o $@
    print("====== ================ =====")


def c_o_files(mod_path, build_dir):
    print("====== Building c files =====")
    cmd = [CC] + CFLAGS + ["-c"] + ["-o"] + LIBSRC_OBJECTS
    run_subprocess(cmd, cwd=build_dir)
    # ${CC} ${CFLAGS} -c $< -o $@
    print("====== ================ =====")


def move_compiled_files(mod_name, mod_path, build_dir):
    so_file = next((f for f in os.listdir(build_dir) if f.endswith('.so')))
    os.makedirs(f"{mod_path}/_{mod_name}", exist_ok=True)
    shutil.move(f"{build_dir}/{so_file}", f"{mod_path}/_{mod_name}/{so_file}")
    # Add init file for _MOD.so file
    # WARNING: This will override __init__ contents
    with open(f"{mod_path}/_{mod_name}/__init__.py", 'w') as f:
        f.write(f"from _{mod_name} import *")
    # Link _mod file to __init__ file

    # WARNING: This will override __init__ contents
    with open(f"{mod_path}/__init__.py", 'w') as f:
        lines = ["# AUTOGENERATED MODULE IMPORT ----------------",
                 "import sys",
                 "import os",
                 "sys.path.insert(0, f\"{os.path.dirname(os.path.abspath(__file__))}/_%s\")" % mod_name,
                 "# -----------------#"]
        f.write("\n".join(lines))

    shutil.move(f"{build_dir}/{mod_name}.py", f"{mod_path}/f_{mod_name}.py")


def build_so_files(mod_name, mod_path, build_dir):
    print("====== Building so files =====")
    libsrc_a_files(mod_path, build_dir)

    c_o_files(mod_path, build_dir)

    f90_fpp_files(mod_path, build_dir)
    # === Build so file
    cmd = ["f90wrap", "-m", mod_name] + \
        LIBSRC_WRAP_FPP_FILES + ["-k", KIND_MAP, "-v"]
    # f90wrap -m ${PYTHON_MODN} ${LIBSRC_WRAP_FPP_FILES} -k ${KIND_MAP} -v
    run_subprocess(cmd, cwd=build_dir)

    out_files = [f"f90wrap_{f}" for f in LIBSRC_WRAP_FILES]
    cmd = ["f2py-f90wrap", f"--fcompiler={FCOMP}", "--build-dir",
           ".", "-c", "-m", f"_{mod_name}", f"-L.", "-lsrc"] + out_files
    # f2py-f90wrap --fcompiler=gfortran --build-dir . -c -m _pipelinedemo -L. -lsrc f90wrap*.f90
    run_subprocess(cmd, cwd=build_dir)
    move_compiled_files(mod_name, mod_path, build_dir)

    # # === Build so pkg file
    # # TODO: Implement building package file
    # # f90wrap -m ${PYTHON_MODN}_pkg ${LIBSRC_WRAP_FPP_FILES} -k ${KIND_MAP} -v -P
    # # f2py-f90wrap --fcompiler=$(FCOMP) --build-dir . -c -m _${PYTHON_MODN}_pkg -L. -lsrc f90wrap*.f90
    # print("====== ================ =====")


@click.group()
def cli():
    pass


def get_fortran_modules():
    return [("pipeline", "src/pipeline")]


@cli.command()
@click.option("--cleanup", default=False, help="Cleanup build dir after build.")
def build(
    cleanup=False,
):
    f_module_paths = get_fortran_modules()
    for (mod_name, mod_path) in f_module_paths:
        build_dir = f"{mod_path}/{BUILD_DIR_NAME}"
        os.makedirs(build_dir, exist_ok=True)
        shutil.copyfile(KIND_MAP, f"{build_dir}/{KIND_MAP}")
        build_so_files(mod_name, mod_path, build_dir)
    if cleanup:
        _clean()


def _clean():
    print("Cleaning Dir")
    f_module_paths = get_fortran_modules()
    for (mod_name, mod_path) in f_module_paths:
        build_dir = f"{mod_path}/{BUILD_DIR_NAME}"
        try:
            shutil.rmtree(build_dir)
        except Exception:
            pass
    # -rm -f ${LIBSRC_OBJECTS} ${LIBSRC_FPP_FILES} libsrc.a _${PYTHON_MODN}*.so \
    # _${PYTHON_MODN}_pkg.so *.mod *.fpp f90wrap*.f90 f90wrap*.o *.o ${PYTHON_MODN}.py
    # -rm -rf ${PYTHON_MODN}_pkg
    # -rm -rf src.*/ .f2py_f2cmap .libs/ __pycache__/


@cli.command()
def clean():
    _clean()


if __name__ == "__main__":
    cli()
