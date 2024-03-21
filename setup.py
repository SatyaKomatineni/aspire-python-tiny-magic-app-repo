from setuptools import setup, find_packages

setup(
    name='aspire_tinyapp',
    version='0.1',
    package_dir={'': 'src'},  # Specifies the directory for the root package(s)
    packages=find_packages(where='src'),  # Tells setuptools to look for packages in 'src'
)
