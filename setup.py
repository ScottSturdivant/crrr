"""
The CRRR website.
"""


from setuptools import setup, find_packages

requires = [
        'Flask',
        'Flask-WTF',
        'pytest',
        'Flask-Mail',
        'Flask-Sqlalchemy',
        'Flask-Login',
        ]

setup(
    author='Scott Sturdivant',
    author_email='scott.sturdivant@gmail.com',
    name="Colorado Rhodesian Ridgeback Rescue",
    version='1.0',
    long_description=__doc__,
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=requires,
    entry_points={
        'console_scripts' : [
            'crrr_import = crrr.scripts.populate_tables:main'
            ]
        }
)
