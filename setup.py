from setuptools import setup, find_packages


def get_requirements(filename):
    """Method to get the requirements of the specified file."""
    file = open(filename, 'r').readlines()
    out = []
    for a in file:
        out.append(a.strip())
    return out


requirements = get_requirements('requirements.txt')
setup(
    name="pynnotate",
    version="0.2",
    packages=find_packages(),
    scripts=['pynnotate.py', ],

    # Project uses reStructuredText, so ensure that the docutils get
    # installed or upgraded on the target machine
    install_requires=requirements,

    package_data={
        # If any package contains *.txt or *.rst files, include them:
        'pynnotate': ['*.txt', '*.rst'],
        # And include any *.msg files found in the 'hello' package, too:
        'hello': ['*.msg'],
    },

    # metadata to display on PyPI
    author="Abhay Raizada",
    author_email="toabhayraizada@gmail.com",
    description="Annotate models based database",
    license="MIT",
    keywords="hello world example examples",
    url="https://github.com/abhsag24/pynnotate",   # project home page, if any
    project_urls={
        "Bug Tracker": "https://github.com/abhsag24/pynnotate/issues",
        "Documentation": "https://github.com/abhsag24/pynnotate/",
        "Source Code": "https://github.com/abhsag24/pynnotate/",
    },
    entry_points={
        "console_scripts": [
            "pynnotate=pynnotate:main"]}
)
