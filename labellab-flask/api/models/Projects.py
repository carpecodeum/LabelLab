from datetime import datetime
from flask import current_app, jsonify

from api.extensions import db, Base
from api.models.Team import Team
from api.models.User import User

ADMIN_TEAMNAME = "admin"
ADMIN_ROLE = "admin"

class Project(db.Model):
    """
    This model holds information about a project and its admin
    """
    __tablename__ = "project"

    id = db.Column(db.Integer, primary_key=True)
    projectname = db.Column(db.String(80), nullable=False,)
    projectdescription = db.Column(db.String(128),
                                default = 'Image labelling')
    admin_id = db.Column(db.Integer, 
                      db.ForeignKey('user.id', ondelete="cascade", onupdate="cascade"),
                      nullable=False)
    labels = db.relationship('Label', 
                             backref='project',
                             lazy=True,
                             cascade="all, save-update, delete",
                             passive_deletes=True)
    images = db.relationship('Image', 
                             backref='project',
                             lazy=True,
                             cascade="all, save-update, delete",
                             passive_deletes=True)
    
    def __init__(self, projectname, projectdescription, admin_id):
        """
        Initializes the project instance
        """
        self.projectname = projectname
        self.projectdescription = projectdescription
        self.admin_id = admin_id

    def __repr__(self):
        """
        Returns the object reprensentation
        """
        return "<Project(projectName='%s', projectId='%s', projectDescription='%s')>" % (self.projectname, self.id, self.projectdescription)
    
    def to_json(self):
        """
        Returns a JSON object
        """
        project_json = {"projectId": self.id, 
                        "projectName": self.projectname}
        return project_json
    
    @classmethod
    def find_by_project_id(cls, id):
        return cls.query.filter_by(id=id).first()
    
    @classmethod
    def find_by_project_name(cls, projectname):
        return cls.query.filter_by(projectname=projectname).first()
    
    @classmethod
    def find_all_projects(cls, admin_id):
        return cls.query.filter_by(admin_id=admin_id).first()
    
    def save(self):
        """
        Save a project to the database.
        This includes creating a new user and editing one.
        """
        try:
            db.session.add(self)
            db.session.commit()
            user = db.session.query(User).filter(User.id == self.admin_id).first()
            print(user)
            project_json = {"projectId": self.id, 
                            "projectName": self.projectname,
                            }
            return project_json
        except Exception as err:
            print("Error occured: ", err)
            response = {"message": "Something went wrong!!"}
            return jsonify(response)
        
