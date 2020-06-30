from setuptools import setup, find_packages

setup(
    name='accounting_vasco',
    packages=['accounting_vasco'],
    version='0.1.0',
    description='Generate VASCO KN-21 XML export for accounting software ',
    author='Boris Savic',
    author_email='boris70@gmail.com',
    url='https://github.com/boris-savic/python-accounting-vasco',
    download_url='https://github.com/boris-savic/python-accounting-vasco/tarball/0.1.0',
    keywords=['python vasco', 'accounting', 'vasco'],
    classifiers=[],
    install_requires=[
        'lxml>=4.5.1',
        'iso3166>=1.0.1'
    ]
)
