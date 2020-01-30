import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pymoos", # Replace with your own username
    version="2020.1.0",
    author="Russ Webber",
    author_email="russ@rw.id.au",
    description="Python bindings for MOOS",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/russkel/pymoos",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: C++",
        "Topic :: Scientific/Engineering"
    ],
    python_requires='>=3.6',
)