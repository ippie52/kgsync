## -----------------------------------------------------------------------------
#  \file   setup.py
#  \brief  Installs the kgsync module
#
# ------------------------------------------------------------------------------
#                  Kris Dunning ippie52@gmail.com 2016.
# ------------------------------------------------------------------------------

from distutils.core import setup
from os import name

if name == 'nt': # It's Windows
    import py2exe

setup(name='kgsync',
      version='0.1',
      description='Git synchroniser tool for managing sub-repositories without using git\'s submodule feature',
      author='Kris Dunning',
      author_email='ippie52@gmail.com',
      url='https://github.com/ippie52/kgsync.git',
      py_modules=['kgsync'],
      console=['kgsync'])