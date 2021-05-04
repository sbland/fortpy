"""Setup main.


NOTE: Must run `./build_fortran` first
"""

import setuptools
from numpy.distutils.core import setup, Extension

with open("README.md", "r") as fh:
    long_description = fh.read()

fortran_modules = [
    # Extension(name="pyprod", sources=["src/prod.f90"]),
    # Extension(name="ftiming", sources=["src/timing.f90"]),
    Extension(
        name="fewert",
        # sources =>  files to by wrapped for python access
        sources=[
            "src/ewert.f90",
        ],
        # extra_objects => Dependencies of sources
        extra_objects=[
            "src/ewert_types.f90",
            "src/ewert_helpers.f90",
        ],
    ),
    # Extension(
    #     name="parentF",
    #     # sources =>  files to by wrapped for python access
    #     sources=[
    #         # "src/ewert_types.f90",
    #         # "src/ewert_helpers.f90",
    #         # "src/child.f90",
    #         "src/parent.f90",
    #     ],
    #     # extra_objects => Dependencies of sources
    #     extra_objects=[
    #         "src/child.f90",
    #     ],
    # ),
]


setup(
    name="fortpy",
    version="0.0.1",
    author="sbland",
    author_email="sbland.co.uk@gmail.com",
    description="Fortran Python Demo",
    setup_requires=[
        'pytest-cov',
        'pytest-runner',
        'snapshottest',
        'numpy'
    ],
    install_requires=['numpy'],
    tests_require=['pytest', 'numpy', 'pandas', 'matplotlib'],
    extras_require={'test': ['pytest', 'numpy', 'pandas']},
    packages=setuptools.find_packages(),
    package_dir={'fortpy': 'fortpy'},
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "Operating System :: OS Independent",
    ],
    ext_modules=fortran_modules
)
