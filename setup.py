from setuptools import setup

setup(
    name="Wikipedia.StrepHit",
    version="1.0",
    py_modules=['strephit'],
    install_requires=[
        'Click',
    ],
    entry_points='''
        [console_scripts]
        strephit=strephit:cli
    ''',
)