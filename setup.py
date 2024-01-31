from setuptools import setup, find_packages

import sys
if sys.version_info < (3, 9):
    sys.exit("Only Python3.9 or above is supported")


setup(
    name="pydocit",
    version="0.1",
    packages=find_packages(),
    install_requires=[],
    python_requires=">3.9",
    author="Ayush K M",
    author_email="ayushkm0000@gmail.com",
    description=" ",
    url="https://github.com/ayuzzh/pydocit",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
