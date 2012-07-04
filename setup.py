"""
The CRRR website.
"""


from setuptools import setup, find_packages

setup(
    author='Scott Sturdivant',
    author_email='scott.sturdivant@gmail.com',
    name="Colorado Rhodesian Ridgeback Rescue",
    version='1.0',
    long_description=__doc__,
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=['Flask', 'Flask-WTF', 'pytest'],
)
