from datetime import datetime
from flask import current_app

from api.extensions import db, Base

class PojectMember(db.Model):
    """
    This model holds information about a projectmember registered
    """
    __tablename__ = "projectmember"

    user_id = db.Column(db.Integer,
                     db.ForeignKey('user.id'), 
                     primary_key=True,
                     nullable=False)
    team_id = db.Column(db.Integer,
                     db.ForeignKey('team.id'), 
                     nullable=False)
    
    def __init__(self, user_id, project_id, team_id):
        """
        Initializes the projectMember instance
        """
        self.user_id = user_id
        self.project_id= project_id
        self.team_id = team_id

    def __repr__(self):
        """
        Returns the object reprensentation
        """
        return "<ProjectMember %r>" % self.user_id
