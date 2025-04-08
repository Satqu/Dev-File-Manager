from setuptools import setup, find_packages

setup(
    name="file_manager",
    version="0.1",
    packages=find_packages(),
    install_requires=['click'],
    python_requires='>=3.6',
)