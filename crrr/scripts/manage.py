from flask.ext.script import Manager, Shell
from crrr import app, db


def _make_context():
    return dict(app=app, db=db)


manager = Manager(app)
manager.add_command('shell', Shell(make_context=_make_context))


def main():
    manager.run()


if __name__ == '__main__':
    main()
