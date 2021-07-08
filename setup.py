from distutils.core import setup
from Cython.Build import cythonize
 
setup(
  name = 'File Name To PinYin',
  ext_modules = cythonize("fname2pinyin.py"),
)
