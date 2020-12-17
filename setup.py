from setuptools import setup, find_packages

with open('README.md') as f:
    long_description = f.read()

setup(
    name='pysnapshot',
    version='0.1.0a',
    classifiers=[
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: Science/Research',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.7',
        'Topic :: Artistic Software',
        'Topic :: Multimedia',
        'Topic :: Multimedia :: Sound/Audio',
        'Topic :: Multimedia :: Sound/Audio :: Editors',
        'Topic :: Software Development :: Libraries',
    ],
    description='Take snapshots of your codebase and reload them easily later.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Prem Seetharaman',
    author_email='prem@descript.com',
    url='https://github.com/pseeth/pysnapshot',
    license='MIT',
    packages=find_packages(),
    keywords=['machine learning', 'experimentation'],
    install_requires=[

    ],
)
