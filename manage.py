#! /usr/bin/env python3

import os

from flask_migrate import Migrate, MigrateCommand
from flask_script import Server, Manager

from wiim import create_app
from wiim.api import db

config = {
    'development': 'wiim.settings.DevelopmentConfig',
    'production': 'wiim.settings.ProductionConfig',
    'testing': 'wiim.settings.TestingConfig'
}

app = create_app(config[os.getenv('WIIM_ENV') or 'development'])
app.app_context().push()

manager = Manager(app)
migrate = Migrate(app, db)

# add database migrate command
manager.add_command('db', MigrateCommand)
# add server command
manager.add_command('run', Server())


@manager.command
def routes():
    import urllib

    output = []
    count = 0

    for rule in app.url_map.iter_rules():
        count += 1
        methods = ','.join(rule.methods)
        line = urllib.parse.unquote(
            "{:3}. {:40s} {:20s} {}".format(count, rule.endpoint, methods, rule)
        )
        output.append(line)

    for line in sorted(output):
        print(line)


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
