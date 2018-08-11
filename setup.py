import os
from distutils.core import setup

if os.name == 'nt':
    OS_INCLUDES = ['pypiwin32']
else:
    OS_INCLUDES = []

setup(
    name='envirosave',
    author='csm10495',
    author_email='csm10495@gmail.com',
    url='http://github.com/csm10495/envirosave',
    version='0.1a',
    packages=['envirosave'],
    license='MIT License',
    python_requires='>=2.7',
    long_description=open('README.md').read(),
    classifiers=[
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    include_package_data = True,
    install_requires=['dill', 'mem_top', 'mss', 'six', 'psutil'] + OS_INCLUDES,
    #entry_points={
    #    'console_scripts': [
    #        'pyrw = ?' # todo... interactive?
    #    ]
    #},
)