from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="olygeo",
    version="0.2.1",
    author="Hyeongjoe Chu",
    author_email="you@example.com",
    description="A geometry library for olympiad-style constructions and proofs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jerrome2685/olygeo",
    packages=find_packages(),
    install_requires=[
        "sympy>=1.8",
        "mpmath>=1.2",
        "multimethod>=1.7"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Mathematics"
    ],
    python_requires='>=3.8',
)
