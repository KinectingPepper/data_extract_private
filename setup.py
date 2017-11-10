from setuptools import setup

setup(name='data_extraction',
      version='0.1',
      description='extracts data',
      author='Thijs Koot',
      license='GPL',
      packages=['data_extraction'],
      install_requires=[
          'pandas',
          'matplotlib'
      ],
      zip_safe=False)