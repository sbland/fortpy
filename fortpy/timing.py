# %%
import timeit
import re
import cProfile
from ftiming import timing


def py_fn(imin, imax):
    n_fact = 1
    for i in range(imin, imax):
        if n_fact < imax:
            n_fact = n_fact + i
        else:
            n_fact = imin

    return n_fact


imin = 1
imax = 10

a = timing.runme(imin, imax - 1)
b = py_fn(imin, imax)
a, b

# %%

imin = 1
imax = 100000


def run_py():
    b = py_fn(imin, imax)


def run_fort():
    a = timing.runme(imin, imax - 1)


out_fort = min(timeit.repeat(run_fort, repeat=10, number=10))
out_fort


out_py = min(timeit.repeat(run_py, repeat=10, number=10))
out_py
out_py - out_fort
# %%
cProfile.run(run_fort)
