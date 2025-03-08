#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="pyciudad",
    version="0.1.0",
    author="PedroOrtix",
    author_email="pedro.ortiz@alumnos.upm.es",
    description="Librería Python para la API REST de CartoCiudad",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/PedroOrtix/pyciudad",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Scientific/Engineering :: GIS",
    ],
    python_requires=">=3.11",
    install_requires=[
        "requests>=2.25.0",
        "pydantic>=2.0.0",
        "typing-extensions>=4.0.0",
    ],
    keywords="cartociudad, geocoding, spain, ign, api, rest, geospatial",
) 