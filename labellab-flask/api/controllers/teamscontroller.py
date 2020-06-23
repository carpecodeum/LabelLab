from flask.views import MethodView
from flask import make_response, request, jsonify, current_app
from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity,
    get_raw_jwt
)
from api.models.Team import Team
from api.models.ProjectMembers import ProjectMember
from api.helpers.user import (
    get_user_roles,
    get_data,
    find_by_email,
    to_json
)
from api.helpers.team import (
    save as save_team, 
    find_by_id,
    delete_by_id as delete_team
)
from api.helpers.projectmember import (
    save as save_projectmember, 
    find_by_user_id_team_id, 
    delete_by_user_id_team_id, 
    count_users_in_team
)
            
class GetAllTeams(MethodView):
    """This class-based view handles fetching of all teams in which the logged in user is a part"""
    
    @jwt_required
    def get(self):
        """Handle GET request for this view. Url ---> /api/v1/team/get"""
        current_user = get_jwt_identity()
        
        try:
            data = get_data(current_user)

            if not data:
                response = {
                    "success": False,
                    "msg": "Data could not be fetched"}
                return make_response(jsonify(response)), 404

            all_teams = data["all_teams"]

            if not all_teams:
                response = {
                    "success": False,
                    "msg": "Data could not be fetched"
                    }
                return make_response(jsonify(response)), 404

            response = {
            "success": True,
            "msg": "Projects fetched successfully.",
            "body": all_teams
            }

            return make_response(jsonify(response)), 200

        except Exception as err:
            print("Error occured: ", err)
            response = {
                "success": False,
                "msg": "Data could not be fetched."
                }
            return make_response(jsonify(response)), 404

class TeamInfo(MethodView):
    """This class handles deletion, updating and fetching a team."""
    @jwt_required
    def get(self, project_id, team_id):
        """Handle GET request for this view. Url --> /api/v1/team/team_info/<int:project_id>/<int:team_id>"""
        try:
            if not team_id:
                response = {
                    "success": False,
                    "msg": "Provide all the required data."
                }
                return make_response(jsonify(response)), 500
            team = find_by_id(team_id)
            if not team:
                response = {
                    "success": False,
                    "msg": "Team not found."
                }
                return make_response(jsonify(response)), 404
            
            response = {
                "success": True,
                "msg": "Team found.",
                "body": team
            }
            return make_response(jsonify(response)), 200
        except Exception:
            response = {
                "success": False,
                "msg": "Something went wrong!!"
            }
            return make_response(jsonify(response)), 404
    
    @jwt_required
    def delete(self, project_id, team_id):
        """Handle DELETE request for this view. Url --> /api/v1/team/team_info/<int:project_id>/<int:team_id>"""
        current_user = get_jwt_identity
        roles = get_user_roles(current_user, project_id)
        
        if not roles.index("admin"):
            print("Error occured: user not admin")
            response = {
                    "success": False,
                    "msg": "User not admin."
                }
            return make_response(jsonify(response)), 400
        try:
            if not team_id:
                response = {
                    "success": False,
                    "msg": "Provide all the required data."
                }
                return make_response(jsonify(response)), 500
            delete_team(team_id)
            response = {
                "success": True,
                "msg": "Team deleted."
            }
            return make_response(jsonify(response)), 200
    
    @jwt_required
    def put(self, project_id, team_id):
        """Handle PUT request for this view. Url --> /api/v1/team/team_info/<int:project_id>/<int:team_id>"""
        # getting JSON data from request
        post_data = request.get_json(silent=True,
                                     force=True)
        current_user = get_jwt_identity
        roles = get_user_roles(current_user, project_id)
        
        if not roles.index("admin"):
            print("Error occured: user not admin")
            response = {
                    "success": False,
                    "msg": "User not admin."
                }
            return make_response(jsonify(response)), 400
        try:
            team_name = post_data["teamname"]
            role = post_data["role"]
        except Exception:
            response = {
                "success": False,
                "msg": "Please provide all the required fields."}
            return make_response(jsonify(response)), 404
        
        try:
            if not (team_id):
                response = {
                    "success": False,
                    "msg": "Provide all the required data."
                }
                return make_response(jsonify(response)), 500
            team = find_by_id(team_id)
            if not team:
                response = {
                    "success": False,
                    "msg": "Team not present."}
                return make_response(jsonify(response)), 404
            
            team['teamname'] = team_name
            team['role'] = role
            
            team_new = save_team(team)
            response = {
                "success": True,
                "msg": "Team updated!!",
                "body": team_new
            }
            return make_response(jsonify(response)), 201
        except Exception as err:
            print("Error occured: ", err)
            response = {
                "success": False,
                "msg": "Something went wrong!!"
            }
            return make_response(jsonify(response)), 500

class AddTeamMember(MethodView):
    """
    This method adds a member to the team.
    """
    @jwt_required
    def post(self, project_id, team_id):
        """
        Handle POST request for this view.
        Url --> /api/v1/team/add_team_member/<int:project_id>/<int:team_id>
        """
        # getting JSON data from request
        post_data = request.get_json(silent=True,
                                     force=True)
        current_user = get_jwt_identity
        roles = get_user_roles(current_user, project_id)

        if not roles.index("admin"):
            print("Error occured: user not admin")
            response = {
                    "success": False,
                    "msg": "User not admin."
                }
            return make_response(jsonify(response)), 400

        try:
            user_email = post_data["memberEmail"]
            user_obj = find_by_email(user_email)
            user = to_json(user_obj)
            if not user:
                response = {
                    "success": False,
                    "msg": "User not found."
                }
                return make_response(jsonify(response)), 404
            
            team = find_by_id(team_id)

            if not team_exist:
                response = {
                    "success": False,
                    "msg": "Team does not exist."
                }
                return make_response(jsonify(response)), 404
            
            project_member = save_projectmember(user['id'], team['id'])
            team_new = find_by_id(project_member['team_id'])
            
            res = {
                "project_member": project_member,
                "team": team_new
            }
            response = {
                "success": True,
                "msg": "Team member added.",
                "body": res
            }
            return make_response(jsonify(response)), 201

        except Exception:
            response = {
                "success": False,
                "msg": "Could not save team member."
            }
            return make_response(jsonify(response)), 500

class RemoveTeamMember(MethodView):
    """
    This method removes a member from a team.
    """
    @jwt_required
    def post(self, project_id, team_id):
        """
        Handle POST request for this view.
        Url --> /api/v1/team/remove_team_member/<int:project_id>/<int:team_id>
        """
        # getting JSON data from request
        post_data = request.get_json(silent=True,
                                     force=True)
        current_user = get_jwt_identity
        roles = get_user_roles(current_user, project_id)

        if not roles.index("admin"):
            print("Error occured: user not admin")
            response = {
                    "success": False,
                    "msg": "User not admin."
                }
            return make_response(jsonify(response)), 400

        try:
            user_email = post_data["memberEmail"]
            user_obj = find_by_email(user_email)
            user = to_json(user_obj)
            if not user:
                response = {
                    "success": False,
                    "msg": "User not found."
                }
                return make_response(jsonify(response)), 404
            try:
                delete_by_user_id_team_id(user['id'], team_id)
                project_members = count_users_in_team(team_id)
                if project_members==0:
                    delete_team(team_id)
                    
                response = {
                    "success": True,
                    "msg": "Team member deleted."
                }
                return make_response(jsonify(response)), 200

            except Exception:
                response = {
                    "success": False,
                    "msg": "Could not delete projectmember from all teams"}
                return make_response(jsonify(response)), 400

        except Exception:
            response = {
                "success": False,
                "msg": "Please provide all the required fields."}
            return make_response(jsonify(response)), 404


teamController = {
    "get_all_teams": GetAllTeams.as_view("get_all_teams"),
    "team": TeamInfo.as_view("team"),
    "add_team_member": AddTeamMember.as_view("add_team_member"),
    "remove_team_member": RemoveTeamMember.as_view("remove_team_member"),
}