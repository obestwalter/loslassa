"""
Loslassa
========

Loslassa provides a simple way to generate static web pages with
Python, reStructuredText, git and love :)

Loslassa is easy to get started
-------------------------------

.. code-block:: bash

    ## todo ##

And Easy to Setup
-----------------

::

    $ pip install Loslassa
    $ loslassa start my_new_website
     "my_new_website" was loslassa ...
     ### todo ###

Links
-----

* ## todo ##

"""
from setuptools import Command, setup

setup(
    name='Loslassa',
    version='0.1-dev',
    url='http://github.com/obestwalter/loslassa/',
    license='DBAD',
    author='Oliver Bestwalter',
    author_email='oliver@bestwalter.de',
    description='A simple way to generate static web pages with '
                'Python, reStructuredText, git and love :)',
    long_description=__doc__,
    packages=['loslassa', 'loslassa.testsuite'],
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    install_requires=[
        'sphinx',
        '## some git bindings ##'
    ],
    classifiers=[
        'Development Status :: 1 - Planning',
        'Environment :: Console',
        'Intended Audience :: Other Audience',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Topic :: Text Processing :: Markup :: HTML',
        'Topic :: Internet :: WWW/HTTP',
    ],
    #cmdclass={},
    test_suite='loslassa.testsuite.suite'
)
