import pkg_resources
from flask.ext.script import Manager, Shell
from flask.ext.migrate import Migrate, MigrateCommand

from crrr import app, db


def _make_context():
    return dict(app=app, db=db)

directory = pkg_resources.resource_filename('crrr', 'migrations')
Migrate(app, db, directory=directory)

manager = Manager(app)
manager.add_command('shell', Shell(make_context=_make_context))
manager.add_command('alembic', MigrateCommand)


def main():
    manager.run()


if __name__ == '__main__':
    main()
