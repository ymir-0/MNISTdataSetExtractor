#!/usr/bin/env python3
# import generic modules
from os.path import join, dirname, isdir
from setuptools import setup
from importlib import import_module
from pkgutil import walk_packages
# constants
YGGDRASIL_REP="http://91.121.9.53:81/"
# parse recursively a module
# this code is an adaptation from https://stackoverflow.com/questions/3365740/how-to-import-all-submodules
def import_submodules(package):
    if isinstance(package, str):
        package = import_module(package)
    modules = list()
    for loader, name, is_pkg in walk_packages(package.__path__):
        full_name = package.__name__ + "." + name
        full_path=join(loader.path,name)
        # continue recursion only if module is folder
        if is_pkg and isdir(full_path):
            modules.append(full_name)
            modules=modules+(import_submodules(full_name))
    return modules
# import and parse dedicated module
import minsdatasetextractor
rootPackage=minsdatasetextractor
module_path = join(dirname(__file__), rootPackage.__name__ , "version.py")
version_line = [line for line in open(module_path) if line.startswith("__version__")][0]
__version__ = version_line.split("__version__ = ")[-1][1:][:-2]
modules=[rootPackage.__name__]+import_submodules (rootPackage)
print("loaded modules : " + str(modules))
# define setup parameters
''' WARNING : to have extra files installed in fine relative directory, please :
 - To make "package_data" parameter find files, put them inside a python package planned for deployment.
   For example :
   minsdatasetextractor
   ├── conf
   │   └── minsdatasetextractor.conf
   ├── __init__.py
   ├── minstdatasetextractor.py
   ├── README.txt
   └── version.py
 - Then use parameter "package_data" instead of "data_files":
   "data_files" will put files in "/usr/local/conf" directory, when "package_data" will respect your paths
'''
setup(
    name="MNISTdataSetExtractor",
    version=__version__,
    description="MNIST data set extractor",
    packages=modules,
    dependency_links=[YGGDRASIL_REP+"pythoncommontools",YGGDRASIL_REP+"neuralnetworkcommon"],
    install_requires=["pythoncommontools","neuralnetworkcommon"],
    package_data={"": ["conf/minsdatasetextractor.conf","README.txt"]},
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
)
