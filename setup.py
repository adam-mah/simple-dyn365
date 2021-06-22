import textwrap
from distutils.core import setup

setup(
  name = 'simple-dyn365',
  packages = ['simple_dyn365'],
  version = '1.4',
  license='MIT',
  description = 'A simple Dynamics 365 Web API implementation',
  author = 'Adam Mahameed',
  long_description=textwrap.dedent(open('README.rst', 'r').read()),
  long_description_content_type='text/x-rst',
  author_email = 'adam.mah315@gmail.com',
  url = 'https://github.com/adam-mah/simple-dyn365',
  download_url = 'https://github.com/adam-mah/simple-dyn365/archive/refs/tags/1.4.tar.gz',
  keywords = ['simple', 'dyn365', 'dynamics', 'WebAPI'],
  install_requires=['requests'],
  classifiers=[
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'Intended Audience :: System Administrators',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: Implementation :: PyPy'
  ],
)