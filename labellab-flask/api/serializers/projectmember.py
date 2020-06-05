from api.extensions import db, Base, ma
from api.models.ProjectMembers import ProjectMember

class ProjectMemberSchema(ma.Schema):
    
    class Meta:
        model = ProjectMember
        fields = ("user_id", 
                  "team_id")