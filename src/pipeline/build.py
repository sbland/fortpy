#! ./venv/bin/python
import sys
import shutil
import os
from warnings import warn
import subprocess

BUILD_DIR = "_build_dir"
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
# Python module name
PYTHON_MODN = "pipelinedemo"
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
    print("cmd: [" + " ".join(cmd) + "]")
    with subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=cwd) as p:
        p.wait()
        if p.returncode != 0:
            warn(f"{SRC_DIR} - {PYTHON_MODN} failed {p.stderr.read().decode('utf-8')}")
            if strict:
                raise Exception("Process Failed")


def libsrc_a_files():
    print("====== Building libsrc files =====")
    f90_0_files()
    cmd = LIBTOOL + ["libsrc.a"] + LIBSRC_OBJECTS
    run_subprocess(cmd, cwd=BUILD_DIR)
    # ${LIBTOOL} $@ $?


def f90_fpp_files():
    print("====== Building fpp files =====")
    for (fin, fout) in zip(LIBSRC_FILES, LIBSRC_FPP_FILES):
        cmd = FPP + FPP_F90FLAGS + \
            [f"-J{BUILD_DIR}"] + [fin] + ["-o"] + [fout]
        run_subprocess(cmd)
        shutil.move(fout, f"{BUILD_DIR}/{fout}")
        # ${FPP} ${FPP_F90FLAGS} $<  -o $@
    print("====== ================ =====")


def f90_0_files():
    print("====== Building o files =====")
    for f, o in zip(LIBSRC_FILES, LIBSRC_OBJECTS):
        cmd = [F90] + F90FLAGS + \
            [f"-J{BUILD_DIR}"] + ["-c"] + [f] + ["-o"] + [o]
        run_subprocess(cmd)
        shutil.move(o, f"{BUILD_DIR}/{o}")
    # ${F90} ${F90FLAGS} -c $< -o $@
    print("====== ================ =====")


def c_o_files():
    print("====== Building c files =====")
    cmd = [CC] + CFLAGS + ["-c"] + ["-o"] + LIBSRC_OBJECTS
    run_subprocess(cmd, cwd=BUILD_DIR)
    # ${CC} ${CFLAGS} -c $< -o $@
    print("====== ================ =====")


def build_so_files():
    print("====== Building so files =====")
    libsrc_a_files()

    f90_0_files()
    c_o_files()

    f90_fpp_files()
    # === Build so file
    cmd = ["f90wrap", "-m", PYTHON_MODN] + \
        LIBSRC_WRAP_FPP_FILES + ["-k", KIND_MAP, "-v"]
    # f90wrap -m ${PYTHON_MODN} ${LIBSRC_WRAP_FPP_FILES} -k ${KIND_MAP} -v
    run_subprocess(cmd, cwd=BUILD_DIR)

    out_files = [f"f90wrap_{f}" for f in LIBSRC_WRAP_FILES]
    cmd = ["f2py-f90wrap", f"--fcompiler={FCOMP}", "--build-dir",
           ".", "-c", "-m", f"_{PYTHON_MODN}", f"-L.", "-lsrc"] + out_files
    # f2py-f90wrap --fcompiler=gfortran --build-dir . -c -m _pipelinedemo -L. -lsrc f90wrap*.f90
    run_subprocess(cmd, cwd=BUILD_DIR)

    # === Build so pkg file
    # TODO: Implement building package file
    # f90wrap -m ${PYTHON_MODN}_pkg ${LIBSRC_WRAP_FPP_FILES} -k ${KIND_MAP} -v -P
    # f2py-f90wrap --fcompiler=$(FCOMP) --build-dir . -c -m _${PYTHON_MODN}_pkg -L. -lsrc f90wrap*.f90
    print("====== ================ =====")


def all():
    args = sys.argv[1:]
    if len(args) > 0 and args[0] == "clean":
        return clean()

    os.makedirs(BUILD_DIR, exist_ok=True)
    shutil.copyfile(KIND_MAP, f"{BUILD_DIR}/{KIND_MAP}")
    build_so_files()


def clean():
    print("Cleaning Dir")
    try:
        shutil.rmtree(BUILD_DIR)
    except Exception:
        pass
    # -rm -f ${LIBSRC_OBJECTS} ${LIBSRC_FPP_FILES} libsrc.a _${PYTHON_MODN}*.so \
    # _${PYTHON_MODN}_pkg.so *.mod *.fpp f90wrap*.f90 f90wrap*.o *.o ${PYTHON_MODN}.py
    # -rm -rf ${PYTHON_MODN}_pkg
    # -rm -rf src.*/ .f2py_f2cmap .libs/ __pycache__/


if __name__ == "__main__":
    all()
