from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import uuid 
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from flask_login import LoginManager
from flask_marshmallow import Marshmallow 
import secrets

# set variables for class instantiation
login_manager = LoginManager()
ma = Marshmallow()
db = SQLAlchemy()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):
    id = db.Column(db.String, primary_key=True)
    first_name = db.Column(db.String(150), nullable=True, default='')
    last_name = db.Column(db.String(150), nullable=True, default='')
    email = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String, nullable=False, default='')
    g_auth_verify = db.Column(db.Boolean, default=False)
    token = db.Column(db.String, default='', unique=True)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __init__(self, email, first_name='', last_name='', password='', token='', g_auth_verify=False):
        self.id = self.set_id()
        self.first_name = first_name
        self.last_name = last_name
        self.password = self.set_password(password)
        self.email = email
        self.token = self.set_token(24)
        self.g_auth_verify = g_auth_verify

    def set_token(self, length):
        return secrets.token_hex(length)

    def set_id(self):
        return str(uuid.uuid4())
    
    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)
        return self.pw_hash

    def __repr__(self):
        return f'User {self.email} has been added to the database'

class CodingTempleProject(db.Model):
    id = db.Column(db.String, primary_key=True)
    project_name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    github_link = db.Column(db.String(200), nullable=True)
    programming_languages = db.Column(db.String(200), nullable=False)
    user_token = db.Column(db.String, db.ForeignKey('user.token'), nullable=False)

    def __init__(self, project_name, description, github_link, programming_languages, user_token):
        self.id = self.set_id()
        self.project_name = project_name
        self.description = description
        self.github_link = github_link
        self.programming_languages = programming_languages
        self.user_token = user_token

    def __repr__(self):
        return f'CodingTempleProject {self.project_name} by {self.user_token}'

    def set_id(self):
        return str(uuid.uuid4())

class CurrentProject(db.Model):
    id = db.Column(db.String, primary_key=True)
    project_name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    github_link = db.Column(db.String(200), nullable=True)
    programming_languages = db.Column(db.String(200), nullable=False)
    user_token = db.Column(db.String, db.ForeignKey('user.token'), nullable=False)

    def __init__(self, project_name, description, github_link, programming_languages, user_token):
        self.id = self.set_id()
        self.project_name = project_name
        self.description = description
        self.github_link = github_link
        self.programming_languages = programming_languages
        self.user_token = user_token

    def __repr__(self):
        return f'CurrentProject {self.project_name} by {self.user_token}'

    def set_id(self):
        return str(uuid.uuid4())

class CodingTempleProjectSchema(ma.Schema):
    class Meta:
        fields = ['id', 'project_name', 'description', 'github_link', 'programming_languages']

coding_temple_project_schema = CodingTempleProjectSchema()
coding_temple_projects_schema = CodingTempleProjectSchema(many=True)

class CurrentProjectSchema(ma.Schema):
    class Meta:
        fields = ['id', 'project_name', 'description', 'github_link', 'programming_languages']

current_project_schema = CurrentProjectSchema()
current_projects_schema = CurrentProjectSchema(many=True)
