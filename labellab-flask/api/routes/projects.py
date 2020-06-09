from flask import Blueprint

from api.controllers import projectscontroller

projectsprint = Blueprint("projects", __name__)

projectsprint.add_url_rule(
    "/project/create", 
    view_func=projectscontroller.projectsController["createproject"], 
    methods=["POST"]
)

# usersprint.add_url_rule(
#     "/auth/register", 
#     view_func=userscontroller.userController["register"], 
#     methods=["POST"]
# )