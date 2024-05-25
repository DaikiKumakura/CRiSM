from setuptools import setup, find_packages

setup(
    name='CRiSM',
    version='0.1.6',
    author='Daiki Kumakura',
    author_email='kmkr.daiki@gmail.com',
    description=('Concatenated Ribosomal Sequence Marker gene analysis tool '
                 'for CPR and other prokaryotic genomes'),
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/DaikiKumakura/CRiSM',
    packages=find_packages(),
    install_requires=[
        'numpy'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    entry_points={
        'console_scripts': [
            'crism=crism.cli:main',  # Ensure 'crism.cli:main' is correctly pointing to the entry function
        ],
    },
    include_package_data=True,
    package_data={
        'crism': ['data/*', 'scripts/*'],
    },
    keywords='bioinformatics phylogenetics genomics CPR ribosome CRiSM bacteria',
    license='MIT',
    project_urls={
        'Documentation': 'https://github.com/DaikiKumakura/CRiSM/README.md',  # Optional if you have specific documentation site
        'Source': 'https://github.com/DaikiKumakura/CRiSM',
        'Tracker': 'https://github.com/DaikiKumakura/CRiSM/issues',
    },
)
