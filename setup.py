from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="screwvina",
    version="1.0.0",
    author="Serena Francisco",
    author_email="serena.francisco@unito.it",
    description="Automated ensemble docking and virtual screening with AutoDock-Vina",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/serenafrancisco/ScrewVina",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
        "Topic :: Scientific/Engineering :: Chemistry",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.9",
    install_requires=[
        # No Python package dependencies!
        # Vina must be installed separately
    ],
    entry_points={
        "console_scripts": [
            "screwvina=screwvina.screwvina:main",
        ],
    },
)
