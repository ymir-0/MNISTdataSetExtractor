#!/usr/bin/env python3
import os

import setuptools

module_path = os.path.join(os.path.dirname(__file__), 'minsdatasetextractor/version.py')
version_line = [line for line in open(module_path)
                if line.startswith('__version__')][0]

__version__ = version_line.split('__version__ = ')[-1][1:][:-2]

setuptools.setup(
    name="MNISTdataSetExtractor",
    version=__version__,
    description="MNIST data set extractor",
    packages=[""],
    dependency_links=["http://91.121.9.53:81/pythoncommontools"], # 91.121.9.53 : yggdrasil
    install_requires=["pythoncommontools"],
    classifiers=[
        'Programming Language :: Python :: 3',
    ],
)
