from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='xlson',
    version='0.0.1',
    author="Denis Moshensky",
    author_email="loven7doo@gmail.com",  
    description="Python package for transforming Excel files to JSON files and manipulating them",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/loven-doo/xlson",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
    ],
    packages=find_packages(),
    package_data={},
    install_requires=[
        'jsondler >= 0.0.1',
        'PyYAML >= 3.13',
        'openpyxl >= 2.5.5, <= 2.5.14',
        'xlrd >= 1.2.0',
        'pillow >= 5.3.0',
    ],
    entry_points={
        'console_scripts': []
    }
)
