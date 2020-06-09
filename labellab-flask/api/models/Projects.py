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

    # def __repr__(self):
    #     """
    #     Returns the object reprensentation
    #     """
    #     return "<Project(projectName='%s', projectId='%s', projectDescription='%s')>" % (self.projectname, self.id, self.projectdescription)
