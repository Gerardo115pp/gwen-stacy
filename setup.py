from setuptools import setup, find_packages

setup( 
    name="patriot-linker",  
    version="0.1",
    author="LiberyLab",
    author_email="contacto@liberylabs.com",
    description="A tool to manage local dependencies for all programing languages, createting templates and linking resources to the project.",
    maintainer="Gerardo Rodriguez Sanchez",
    maintainer_email="gerardo.rodriguez@liberylabs.com",\
    install_requires=["pyyaml", "click"],
    license="GPL-2.0-only",
    packages=find_packages(
        where="src" 
    ),
    entry_points='''
    [console_scripts]
    patriotl=src.main:cli
    '''
)