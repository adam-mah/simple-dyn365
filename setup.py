from distutils.core import setup
setup(
  name = 'simple-dyn365',
  packages = ['simple-dyn365'],   # Chose the same as "name"
  version = '1.0',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'A simple Dynamics 365 WebAPI implementation',   # Give a short description about your library
  author = 'Adam Mahameed',                   # Type in your name
  author_email = 'adam.mah315@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/adam-mah',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/adam-mah/simple-dyn365/archive/refs/heads/main.zip',    # I explain this later on
  keywords = ['simple', 'dyn365', 'dynamics', 'WebAPI'],   # Keywords that define your package best
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