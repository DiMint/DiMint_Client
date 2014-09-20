from setuptools import setup

setup(
    name='dimint-client',
    packages=[
        'dimint',
    ],
    version='0.1',
    description='Python client for DiMint, distributed key-value storage',
    url='https://github.com/DiMint/DiMint_Client',
    author='Kim Jae Chan',
    author_email='kjc0210@snu.ac.kr',
    keywords=[
        'Dimint',
        'distributed key-value storage',
    ],
    install_requires=[
        'pyzmq>=14.3.1',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python 3',
        'Programming Language :: Python 3.2',
        'Programming Language :: Python 3.3',
        'Programming Language :: Python 3.4',
    ]
)
