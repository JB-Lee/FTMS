import io

from setuptools import setup


# Read in the README for the long description on PyPI
def long_description():
    with io.open('README.rst', 'r', encoding='utf-8') as f:
        readme = f.read()
    return readme


setup(name='ftms_lib',
      version='0.1',
      description='ftms_library',
      license='MIT',
      packages=["ftms_lib", "ftms_lib.command", "ftms_lib.utils"],
      classifiers=[
          'Programming Language :: Python :: 3.8',
      ],
      install_reqires=[
          'bson~=0.5.10'
      ],
      zip_safe=False)
