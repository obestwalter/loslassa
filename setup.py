"""

.pypirc should look like this::

    [server-login]
    username:oliver.bestwalter
    password:<wont tell ya>

Release process:
 * update __version__
 * python ./setup.py sdist upload
"""
from setuptools import setup

from loslassa import __version__

with open("requirements.txt") as f:
    requirements = f.readlines()

setup(
    name='Loslassa',
    description='Just another toy static website generator',
    version=__version__,
    license='BSD',
    url='http://github.com/obestwalter/loslassa/',
    author='Oliver Bestwalter',
    author_email='oliver@bestwalter.de',
    long_description='',
    packages=['loslassa'],
    include_package_data=True,
    zip_safe=False,
    platforms='Unix',
    install_requires=requirements,
    entry_points=dict(console_scripts=['loslassa=loslassa._loslassa:main']),
    classifiers=[
        'Development Status :: 3 - Alpha',
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
