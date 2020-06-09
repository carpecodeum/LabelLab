from flask.views import MethodView
from flask import make_response, request, jsonify, current_app
from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity,
    get_raw_jwt
)
from api.models.Projects import Project
from api.models.Team import Team
from api.helpers.project import find_by_projectname, save, find_all_by_admin_id
# from api.helpers.user import find_by_id


class CreateProject(MethodView):
    """This class creates a new project."""
    @jwt_required
    def post(self):
        """Handle POST request for this view. Url --> /api/v1/project/create"""
        # getting JSON data from request
        post_data = request.get_json(silent=True,
                                     force=True)
        current_user = get_jwt_identity()
        try:
            projectname = post_data["projectname"]
            projectdescription = post_data["projectdescription"]
            admin_id = current_user
        except Exception:
            response = {"message": "Please provide all the required fields."}
            return make_response(jsonify(response)), 404

        # Querying the database with requested projectname
        project = find_by_projectname(projectname)

        if project:
            # There is an existing project with the same name. We don't want to create two
            # projects with the same name.
            # Return a message to the user telling them that they have already created a project
            # with this name.
            response = {"message": "Project already exists. Please change the Project Name."}
            return make_response(jsonify(response)), 401
        
        # There is no project so we'll try to create a new one
        
        """Save the new Project."""
        try:
            project = Project(projectname=projectname, 
                        projectdescription=projectdescription, 
                        admin_id=admin_id)
            project_new = save(project)
        except Exception as err:
            print("Error occured: ", err)
            response = {"message": "Something went wrong!!"}
            return make_response(jsonify(response)), 500
        l = find_all_by_admin_id(1)
        response = {
                    "message": "Your project was created successfully.",
                    "project": project_new
                    }
        # return a response notifying the user that they registered
        # successfully
        return make_response(jsonify(response)), 201


class GetAllProjects(MethodView):
    """This class-based view handles fetching of all projects in which the logged in user is an admin."""
    
    @jwt_required
    def get(self):
        """Handle POST request for this view. Url ---> /api/users/login"""
        current_user = get_jwt_identity()
        
        # try:
        #     email = data["email"]
        #     password = data["password"]
        # except Exception as err:
        #     print("Error occured: ", err)
        #     response = {"message": "Please provide all the required fields."}
        #     return make_response(jsonify(response)), 404

        # Get the user object using their email (unique to every user)
        # print(dir(User.User))
        user = User.find_by_email(email)

        if not user:
            # User does not exist. Therefore, we return an error message
            response = {"message": "Invalid email, Please try again"}
            return make_response(jsonify(response)), 401

        # Try to authenticate the found user using their password
        if not user.verify_password(password):
            response = {"message": "Wrong password, Please try again"}
            return make_response(jsonify(response)), 402

        access_token = create_access_token(identity=user.id, fresh=True)
        refresh_token = create_refresh_token(user.id)

        if not access_token or not refresh_token:
            response = {"message": "Something went wrong!"}
            # Return a server error using the HTTP Error Code 500 (Internal
            # Server Error)
            return make_response(jsonify(response)), 500

        # Generate the access token. This will be used as the
        # authorization header
        response = {
            "message": "You logged in successfully.",
            "access_token": access_token,
            "refresh_token": refresh_token,
            "user_details": user.to_json(),
        }
        return make_response(jsonify(response)), 200


# class LogoutAccess(MethodView):
#     """
#     This method removes the access token on logout and stores the revoked token.
#     """
#     @jwt_required
#     def post(self):
#         jti = get_raw_jwt()["jti"]
#         try:
#             revoked_token = RevokedToken(jti=jti)
#             revoked_token.add()
#             response = {"message": "Access token has been revoked"}
#             return make_response(jsonify(response)), 200
#         except Exception:
#             response = {"message": "Something went wrong!"}
#             # Return a server error using the HTTP Error Code 500 (Internal
#             # Server Error)
#             return make_response(jsonify(response)), 500


# class LogoutRefresh(MethodView):
#     """
#     This method removes the refresh token on logout and stores the revoked token.
#     """
#     @jwt_refresh_token_required
#     def post(self):
#         jti = get_raw_jwt()["jti"]
#         try:
#             revoked_token = RevokedToken(jti=jti)
#             revoked_token.add()
#             response = {"message": "Refresh token has been revoked"}
#             return make_response(jsonify(response)), 200
#         except Exception:
#             response = {"message": "Something went wrong!"}
#             # Return a server error using the HTTP Error Code 500 (Internal
#             # Server Error)
#             return make_response(jsonify(response)), 500


# class TokenRefresh(MethodView):
#     """
#     This method is called when the access token is missing or is expired.
#     """
#     @jwt_refresh_token_required
#     def post(self):
#         current_user = get_jwt_identity()
#         access_token = create_access_token(identity=current_user, 
#                                            fresh=False)

#         response = {
#             "message": "Token refreshed successfully",
#             "access_token": access_token,
#         }
#         return make_response(jsonify(response)), 200


projectsController = {
    "createproject": CreateProject.as_view("createproject"),
    # "login": Login.as_view("login"),
    # "logout_access": LogoutAccess.as_view("logout_access"),
    # "logout_refresh": LogoutRefresh.as_view("logout_refresh"),
    # "token_refresh": TokenRefresh.as_view("token_refresh"),
}