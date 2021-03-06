from timbreuse import db
from werkzeug.security import generate_password_hash, \
     check_password_hash


class User(db.Model):
    id = db.Column(db.Integer , primary_key=True)
    username = db.Column('username', db.String(20), unique=True , index=True)
    pw_hash = db.Column('pw_hash' , db.String(66))
    current_project_id = db.Column('current_project_id', db.Integer)
    projects = db.relationship('Project', backref='user', lazy='dynamic')

    def __init__(self, username, password):
        self.username = username
        self.set_password(password)

    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)
        print(self.pw_hash)

    def check_password(self, password):
        return check_password_hash(self.pw_hash, password)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

    def __repr__(self):
        return '<User {}>'.format(self.username)


class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    current_task_id = db.Column('current_task_id', db.Integer)
    tasks = db.relationship('Task', backref='project', lazy='dynamic')

    def __init__(self, name):
        self.name = name


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    description = db.Column(db.Text)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))
    timeslots = db.relationship('TimeSlot', backref='task', lazy='dynamic')

    def __init__(self, name, description):
        self.name = name
        self.description = description


class TimeSlot(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.Text)
    started_at = db.Column(db.DateTime)
    ended_at = db.Column(db.DateTime)
    task_id = db.Column(db.Integer, db.ForeignKey('task.id'))

    def __init__(self, comment, started_at):
        self.comment = comment
        self.started_at = started_at
