import setuptools
from numpy.distutils.core import setup, Extension

with open("README.md", "r") as fh:
    long_description = fh.read()

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
    ext_modules=[
        Extension(name="pyprod", sources=["src/prod.f90"]),
        Extension(name="ftiming", sources=["src/timing.f90"]),
    ]
)
