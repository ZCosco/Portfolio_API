from flask import Blueprint, request, jsonify
from helpers import token_required
from models import db, User, CodingTempleProject, CurrentProject, current_project_schema, current_projects_schema, coding_temple_project_schema, coding_temple_projects_schema

api = Blueprint('api', __name__, url_prefix='/api')

@api.route('/current_projects', methods=['POST'])
@token_required
def create_current_project(current_user_token):
    project_name = request.json['project_name']
    description = request.json['description']
    github_link = request.json['github_link']
    programming_languages = request.json['programming_languages']
    user_token = current_user_token.token
    project = CurrentProject(project_name=project_name, description=description, github_link=github_link,
                             programming_languages=programming_languages, user_token=user_token)
    db.session.add(project)
    db.session.commit()
    response = current_project_schema.dump(project)
    return jsonify(response), 201

@api.route('/current_projects', methods=['GET'])
@token_required
def get_current_projects(current_user_token):
    user_token = current_user_token.token
    projects = CurrentProject.query.filter_by(user_token=user_token).all()
    response = current_projects_schema.dump(projects)
    return jsonify(response)

@api.route('/current_projects/<id>', methods=['GET'])
@token_required
def get_single_current_project(current_user_token, id):
    project = CurrentProject.query.get(id)
    if project:
        response = current_project_schema.dump(project)
        return jsonify(response)
    else:
        return jsonify({'message': 'Project not found'}), 404

@api.route('/current_projects/<id>', methods=['POST', 'PUT'])
@token_required
def update_current_project(current_user_token, id):
    project = CurrentProject.query.get(id)
    if not project:
        return jsonify({'message': 'Project not found'}), 404
    project.project_name = request.json.get('project_name', project.project_name)
    project.description = request.json.get('description', project.description)
    project.github_link = request.json.get('github_link', project.github_link)
    project.programming_languages = request.json.get('programming_languages', project.programming_languages)
    db.session.commit()
    response = current_project_schema.dump(project)
    return jsonify(response)

@api.route('/current_projects/<id>', methods=['DELETE'])
@token_required
def delete_current_project(current_user_token, id):
    project = CurrentProject.query.get(id)
    if not project:
        return jsonify({'message': 'Project not found'}), 404
    db.session.delete(project)
    db.session.commit()
    response = current_project_schema.dump(project)
    return jsonify(response)

@api.route('/coding_temple_projects', methods=['GET'])
@token_required
def get_coding_temple_projects(current_user_token):
    projects = CodingTempleProject.query.all()
    response = coding_temple_projects_schema.dump(projects)
    return jsonify(response)
