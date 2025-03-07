from flask import render_template, request, jsonify
from models import Folder, Link
from app import db, app

@app.route('/')
def index():
    folders = Folder.query.all()
    return render_template('index.html', folders=folders)

@app.route('/folder/<int:folder_id>')
def folder(folder_id):
    folder = Folder.query.get_or_404(folder_id)
    links = Link.query.filter_by(parent_id=folder_id).all()
    folders = Folder.query.all()
    return render_template('folder.html', selected_folder=folder, links=links, folders=folders)

@app.route('/api/folder/<int:folder_id>/links', methods=['GET'])
def get_links(folder_id):
    links = Link.query.filter_by(parent_id=folder_id).all()
    return jsonify([{
        'id': link.id,
        'title': link.title,
        'href': link.href,
        'is_archived': link.is_archived,
        'is_personal': link.is_personal
    } for link in links])

@app.route('/api/link/<int:link_id>', methods=['PUT'])
def update_link(link_id):
    data = request.json
    link = Link.query.get_or_404(link_id)
    link.is_archived = data.get('is_archived', link.is_archived)
    link.is_personal = data.get('is_personal', link.is_personal)
    db.session.commit()
    return jsonify({'message': 'Link updated successfully'})