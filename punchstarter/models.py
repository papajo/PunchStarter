from punchstarter import db, app
from sqlalchemy.sql import func
from flask.ext.security import RoleMixin, UserMixin
import datetime
import cloudinary.utils

roles_members = db.Table('roles_members',
        db.Column('member_id', db.Integer(), db.ForeignKey('member.id')),
        db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))

class Member(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	first_name = db.Column(db.String(64), nullable=False)
	last_name = db.Column(db.String(64), nullable=False)
	email = db.Column(db.String(255), unique=True)
	password = db.Column(db.String(255))
	active = db.Column(db.Boolean())
	confirmed_at = db.Column(db.DateTime())
	project = db.relationship('Project', backref='creator', lazy='dynamic')
	pledges = db.relationship('Pledge', backref='member', lazy='dynamic', foreign_keys='Pledge.member_id')
	roles = db.relationship('Role', secondary=roles_members,
						backref=db.backref('members', lazy='dynamic'))

class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    member_id = db.Column(db.Integer, db.ForeignKey('member.id'), nullable=False)
    name = db.Column(db.String(100))
    short_description = db.Column(db.Text)
    long_description = db.Column(db.Text)
    goal_amount = db.Column(db.Integer)
    image_filename = db.Column(db.String(200))
    time_start = db.Column(db.DateTime)
    time_end = db.Column(db.DateTime)
    time_created = db.Column(db.DateTime)
    pledges = db.relationship('Pledge', backref='project', foreign_keys='Pledge.project_id')

    @property
    def num_pledges(self):
        return len(self.pledges)

    @property
    def total_pledges(self):
        total_pledges = db.session.query(func.sum(Pledge.amount)).filter(Pledge.project_id==self.id).one()[0]
        if total_pledges is None:
            total_pledges = 0
        return total_pledges

    @property
    def num_days_left(self):
        now = datetime.datetime.now()
        num_days_left = (self.time_end - now).days

        return num_days_left

    @property
    def percentage_funded(self):
    	return int(self.total_pledges  * 100 / self.goal_amount)

    @property
    def image_path(self):
        return cloudinary.utils.cloudinary_url(self.image_filename)[0]

class Pledge(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    member_id = db.Column(db.Integer, db.ForeignKey('member.id'), nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    amount = db.Column(db.Integer)
    time_created = db.Column(db.DateTime)
