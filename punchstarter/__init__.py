from flask import Flask, render_template, request, redirect, url_for, abort
from flask.ext.script import Manager
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.migrate import Migrate, MigrateCommand
import datetime
import cloudinary.uploader

app = Flask(__name__)
app.config.from_object('punchstarter.default_settings')
manager = Manager(app)

db = SQLAlchemy(app)
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)

from punchstarter.models import *

#index route
@app.route("/")
def hello():
    return render_template("index.html")

#create a new project route
@app.route("/projects/create/", methods=['GET', 'POST'])
def create():
    if request.method == 'GET':
        return render_template("create.html")
    if request.method == 'POST':
        now = datetime.datetime.now()
        time_end = datetime.datetime.strptime(request.form.get("funding_end_date"), "%Y-%m-%d")

        #Upload cover photo
        cover_photo = request.files['cover_photo']
        uploaded_image = cloudinary.uploader.upload(
        	cover_photo,
        	crop = 'limit',
        	width = 600,
        	height = 550
        )
        image_filename = uploaded_image["public_id"]

        new_project = Project(
            member_id = 1,
            name = request.form.get("project_name"),
            short_description = request.form.get("short_description"),
            long_description = request.form.get("long_description"),
            goal_amount = request.form.get("funding_goal"),
            image_filename = image_filename,
            time_start = now,
            time_end = time_end,
            time_created = now
        )

        db.session.add(new_project)
        db.session.commit()

        return redirect(url_for('project_detail', project_id=new_project.id))

#goto a specific project route
@app.route("/projects/<int:project_id>/")
def project_detail(project_id):
    project = db.session.query(Project).get(project_id)
    if project is None:
        abort(404)

    return render_template('project_detail.html', project=project)

#view pledge route
@app.route("/projects/<int:project_id>/pledge/", methods=['GET', 'POST'])
def pledge(project_id):
    project = db.session.query(Project).get(project_id)
    if project is None:
        abort(404)

    if request.method == 'GET':
        return render_template("pledge.html", project=project)
    #Hardcode guest pledgor for now

    elif request.method == 'POST':
        guest_creator = db.session.query(Member).filter_by(id=2).one()
        new_pledge = Pledge(
            member_id = guest_creator.id,
            project_id = project_id,
            amount = request.form.get('amount'),
            time_created = datetime.datetime.now()
        )
        db.session.add(new_pledge)
        db.session.commit()

        return redirect(url_for('project_detail', project_id=project.id))

@app.route('/search/')
def search():
    query = request.args.get("q") or ""
    projects = db.session.query(Project).filter(
    	Project.name.ilike('%'+query+'%') |
    	Project.short_description.ilike('%'+query+'%') |
    	Project.long_description.ilike('%'+query+'%')
    ).all()
    project_count = len(projects)

    query_text = query if query != "" else "all projects"

    return render_template('search.html',
    	query_text=query_text,
    	projects=projects,
    	project_count=project_count
    )
