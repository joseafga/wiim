#! /usr/bin/env python3

import os

from flask_migrate import Migrate, MigrateCommand
from flask_script import Server, Manager

from wiim import create_app
from wiim.api import db

config = {
    'dev': 'wiim.settings.DevelopmentConfig',
    'prod': 'wiim.settings.ProductionConfig',
    'test': 'wiim.settings.TestingConfig'
}

app = create_app(config[os.getenv('WIIM_ENV') or 'dev'])
app.app_context().push()

manager = Manager(app)
migrate = Migrate(app, db)

# add database migrate command
manager.add_command('db', MigrateCommand)
# add server command
manager.add_command('run', Server())


# @manager.command
# def test():
#     """Runs the unit tests."""
#     tests = unittest.TestLoader().discover('app/test', pattern='test*.py')
#     result = unittest.TextTestRunner(verbosity=2).run(tests)
#     if result.wasSuccessful():
#         return 0
#     return 1


if __name__ == '__main__':
    manager.run()
