"""See README.rst for description"""
from setuptools import setup

from loslassa._loslassa import __doc__, __version__


setup(
    name='Loslassa',
    description=('A simple way to interactively develop web pages with '
                 'reStructuredText and love :)'),
    version=__version__,
    license='BSD',
    url='http://github.com/obestwalter/loslassa/',
    author='Oliver Bestwalter',
    author_email='oliver@bestwalter.de',
    long_description=__doc__,
    packages=['loslassa'],
    include_package_data=True,
    zip_safe=False,
    platforms='Unix',  # todo add windows and Mac Os X
    install_requires=[
        'Sphinx>=1.1.3',
        'plumbum>=1.0',
        'sphinx_bootstrap_theme',
        'pytest>=2.3'
    ],
    entry_points=dict(console_scripts=['loslassa=loslassa._loslassa:main']),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Other Audience',
        'License :: OSI Approved :: BSD License',
        'Operating System :: Unix',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Topic :: Text Processing :: Markup :: HTML',
        'Topic :: Internet :: WWW/HTTP',
    ],
)
