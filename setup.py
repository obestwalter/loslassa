"""See README.rst for description"""
from setuptools import setup

from loslassa.loslassa import __doc__, __version__


setup(
    name='Loslassa',
    description='Web Site generator based on sphinx and git',
    version=__version__,
    license='BSD',
    url='http://github.com/obestwalter/loslassa/',
    author='Oliver Bestwalter',
    author_email='oliver@bestwalter.de',
    long_description=open("README.rst", "w").read(),
    #keywords='',
    packages=['loslassa'],
    include_package_data=True,
    zip_safe=False,
    platforms='Unix', # todo add windows and Mac Os X
    install_requires=['Sphinx>=1.1.3', 'plumbum', 'sphinx_bootstrap_theme'],
    entry_points=dict(console_scripts=['loslassa=loslassa.loslassa:main']),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Other Audience',
        'License :: OSI Approved :: BSD License',
        'Operating System :: Unix',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Topic :: Text Processing :: Markup :: HTML',
        'Topic :: Internet :: WWW/HTTP',
    ],
)
