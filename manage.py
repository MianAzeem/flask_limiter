import uuid
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

DEFAULT_LIMIT = "10/day, 0/minute"

app = Flask(__name__)
# setting db path
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root1234@localhost/test'

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# to apply migrations
manager = Manager(app)
manager.add_command('db', MigrateCommand)

# Company Model
class Company(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    identity = db.Column(db.String(100), unique=True, default=str(uuid.uuid4()))
    limit = db.Column(db.String(50), default=DEFAULT_LIMIT)
    is_active = db.Column(db.Boolean, default=True)

    def __init__(self, name, limit):
        self.name = name
        self.limit = limit


if __name__ == '__main__':
    manager.run()