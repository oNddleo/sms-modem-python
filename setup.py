import os
import sys
from distutils.sysconfig import get_python_lib
from os import path
from setuptools import find_packages, setup

print(sys.version_info[:2])

print(find_packages())
here = path.abspath(path.dirname(__file__))
print('abspath here: ', here)

with open(path.join(here, 'README.md'), 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='SMS Modem',
    version='0.1',
    author = 'LongND',
    author_email = 'nguyenduclong12a2nd@gmail.com',
    url = 'https://github.com/oNddleo/sms-modem-python',
    description='A SMS Modem Python Project',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(exclude=['tests', 'tests.*']),
    package_data={'': ['sms.txt']},
    data_files=[('', ['__main__.py'])],
    include_package_data=True,
    zip_safe=True,
    install_requires=['serial', 'natsort'],
    python_requires='>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*, <4',
    classifiers=[  # Optional
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',

        # Pick your license as you wish
        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        # These classifiers are *not* checked by 'pip install'. See instead
        # 'python_requires' below.
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
)