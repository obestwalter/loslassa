"""See README.rst for description"""
from setuptools import setup

setup(
    name='Loslassa',
    description='Web Site generator based on sphinx and git',
    version='0.1-dev-3',
    license='BSD',
    url='http://github.com/obestwalter/loslassa/',
    author='Oliver Bestwalter',
    author_email='oliver@bestwalter.de',
    long_description=open("README.rst").read(),
    packages=['loslassa', 'loslassa.testsuite'],
    package_data={'loslassa': ["example_project/source/*"]},
    include_package_data=True,
    zip_safe=False,
    platforms='UNIX', # todo add windows and Mac Os X
    install_requires=['Sphinx>=1.1.3', 'plumbum', 'sphinx_bootstrap_theme'],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Console',
        'Intended Audience :: Other Audience',
        'License :: OSI Approved :: BSD License',
        'Operating System :: UNIX',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Topic :: Text Processing :: Markup :: HTML',
        'Topic :: Internet :: WWW/HTTP',
    ],
)
