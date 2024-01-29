import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='RAMACHANDRAN',
    version='0.2.4',
    author='VB',
    author_email='VB@gmail.com',
    description='Ramachandran plotting tool',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/alxdrcirilo/RamachanDraw',
    packages=['RAMACHANDRAN'],
    package_data={'RAMACHANDRAN': ['./density_estimate.dat']},
    install_requires=[
        'biopython>=1.75',
        'matplotlib>=3.1.2',
        'rich>=9.3'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
