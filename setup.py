from setuptools import setup, find_packages
import os


setup( 
    name="gwen-stacy",
    version="0.2",
    author="LiberyLab",
    author_email="contacto@liberylabs.com",
    description="A tool to manage local dependencies for all programing languages, createting templates and linking resources to the project.",
    maintainer="Gerardo Rodriguez Sanchez",
    maintainer_email="gerardo.rodriguez@liberylabs.com",
    install_requires=["pyyaml", "click"],
    license="LGPL-2.1-only",
    # package_dir={'': 'src'},
    packages=find_packages(),
    entry_points='''
    [console_scripts]
    gwen=Gwen:cli
    '''
)