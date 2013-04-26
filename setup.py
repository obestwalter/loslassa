"""See README.rst for description"""
from setuptools import setup

setup(
    name='Loslassa',
    version='0.1-dev-0',
    url='http://github.com/obestwalter/loslassa/',
    license='BSD',
    author='Oliver Bestwalter',
    author_email='oliver@bestwalter.de',
    description='Web Site generator based on sphinx and git',
    long_description=open("README.rst").read(),
    packages=['loslassa', 'loslassa.testsuite'],
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    install_requires=['Sphinx>=1.1.3', 'plumbum', 'sphinx_bootstrap_theme'],
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
)
