from flask import Blueprint, render_template
from models import CodingTempleProject

site = Blueprint('site', __name__, template_folder='site_templates')


@site.route('/')
def home():
    coding_temple_projects = CodingTempleProject.query.all()
    return render_template('index.html', coding_temple_projects=coding_temple_projects)

@site.route('/profile')
def profile():
    return render_template('profile.html')