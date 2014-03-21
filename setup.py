from distutils.core import setup

setup(
    name='django-admin-genericfk',
    version='0.1dev',
    packages=['admin_genericfk'],
    install_requires=['django'],
    license='Creative Commons Attribution-Noncommercial-Share Alike license',
    long_description=open('README.rst').read(),
)
