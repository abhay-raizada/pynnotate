from setuptools import setup, find_packages
import os

def get_requirements(filename):
    """Method to get the requirements of the specified file."""
    file = open(filename, 'r').readlines()
    out = []
    for a in file:
        out.append(a.strip())
    return out

def get_packages():
    """Method to retrieve packages to be bundled."""
    base_dir = '.'
    packages = [base_dir]
    for (path, dirs, files) in os.walk(base_dir):
        try:
            dirs.remove('__pycache__')
        except ValueError:
            pass
        if '__init__.py' in files:
            packages.extend([os.path.join(path, dir) for dir in dirs])
    return packages

requirements = get_requirements('requirements.txt')
setup(
    name="orator-annotate",
    version="0.1.2",
    packages=get_packages(),
    scripts=['orator_annotate.py'],

    # Project uses reStructuredText, so ensure that the docutils get
    # installed or upgraded on the target machine
    install_requires=requirements,

    package_data={
        # If any package contains *.txt or *.rst files, include them:
        '': ['*.txt', '*.rst'],
        # And include any *.msg files found in the 'hello' package, too:
        'hello': ['*.msg'],
    },

    # metadata to display on PyPI
    author="Abhay Raizada",
    author_email="toabhayraizada@gmail.com",
    description="Annotate models based database",
    license="MIT",
    keywords="hello world example examples",
    url="https://github.com/abhsag24/orator-annotate",   # project home page, if any
    project_urls={
        "Bug Tracker": "https://github.com/abhsag24/orator-annotate/issues",
        "Documentation": "https://github.com/abhsag24/orator-annotate/",
        "Source Code": "https://github.com/abhsag24/orator-annotate/",
    },
    entry_points={
        "console_scripts": [
                  "orator-annotate=orator_annotate:main"]}
)
