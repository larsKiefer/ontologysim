import pathlib

from pkg_resources import parse_requirements
from setuptools import setup, find_packages
import os

tensorforce_directory = os.path.abspath(os.path.dirname(__file__))

install_reqs = parse_requirements("requirements.txt")
# Extract install_requires from requirements.txt
install_requires = list()
with open(os.path.join(tensorforce_directory, 'requirements.txt'), 'r') as filehandle:
    for line in filehandle:
        line = line.strip()
        if line:
            install_requires.append(line)
assert len(install_requires) > 0

setup(
    name='ontologysim',
    version='1.0.1',
    license='GPLv3',
    author="Lars Kiefer, Marvin Carl May",
    author_email='lars.kiefer@alumni.kit.edu',
    packages=find_packages( exclude=("tests","example","ontologysim/testPlayground")),
    package_dir={"ontologysim":"ontologysim"},
    url='https://github.com/larsKiefer/ontologysim',
    description='',
    project_urls ={
      'Documentation': 'https://ontologysim.readthedocs.io/en/latest/',
      'Frontend': 'https://github.com/larsKiefer/ontologysim_react',

    },
    python_requires='>=3.7',
    classifiers=[
        'Natural Language :: English',
        'Topic :: Scientific/Engineering',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8'
    ],
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    keywords='ontology, manufacturing, simulation',
    install_requires=install_requires,

    include_package_data=True,


)