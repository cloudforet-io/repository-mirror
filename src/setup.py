from setuptools import setup, find_packages

with open('VERSION', 'r') as f:
    VERSION = f.read().strip()
    f.close()

setup(
    name='repository-mirror',
    version=VERSION,
    description='Cloudforet Sync repository tools',
    long_description='',
    url='https://cloudforet.io/',
    author='MEGAZONE SpaceONE Team',
    author_email='admin@spaceone.dev',
    license='Apache License 2.0',
    packages=find_packages(),
    install_requires=[
        'spaceone-core',
        'spaceone-api',
        'click',
        'tabulate'
    ],
    zip_safe=False,
    entry_points={
        'console_scripts': [
            'repository-mirror = repository_mirror.main:main',
        ]
    },
)