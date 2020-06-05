from api.extensions import db, Base, ma
from api.models.Projects import Project

class ProjectSchema(ma.Schema):
    
    class Meta:
        model = Project
        fields = ("id", 
                  "projectname", 
                  "projectdescription",
                  "admin_id")