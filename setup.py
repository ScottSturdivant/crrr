"""
The CRRR website.
"""
import glob
from setuptools import setup, find_packages


def get_requirements(suffix=''):
    with open('requirements%s.txt' % suffix) as f:
        return [line.strip() for line in f if not line.startswith('#')]

setup(
    author='Scott Sturdivant',
    author_email='scott.sturdivant@gmail.com',
    name="Colorado Rhodesian Ridgeback Rescue",
    version='1.1.0',
    long_description=__doc__,
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=get_requirements(),
    package_data={'crrr': glob.glob('migrations/*.py') +
                  glob.glob('migrations/*.mako') +
                  glob.glob('migrations/versions/*.py') +
                  ['migrations/alembic.ini']},
    entry_points={
        'console_scripts': [
            'crrr_import = crrr.scripts.populate_tables:main',
            'crrr_add_admin_user = crrr.scripts.add_admin:main',
            'crrr_manage = crrr.scripts.manage:main',
        ]
    }
)
