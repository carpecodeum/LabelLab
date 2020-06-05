from api.extensions import db, Base, ma
from api.models.User import User
from api.serializers.project import ProjectSchema
from api.serializers.projectmember import ProjectMemberSchema

class UserSchema(ma.Schema):
    
    projects = ProjectSchema(many=True)
    projectmembers = ProjectMemberSchema(many=True)
    
    class Meta:
        model = User
        fields = ("id", 
                  "name", 
                  "username",
                  "email",
                  "thumbnail",
                  "projects",
                  "projectmembers")

# user_schema = UserSchema()
# users_schema = UserSchema(many=True)





# #adding a post
# @app.route('/post', methods = ['POST'])
# def add_post():
#     title = request.json['title']
#     description = request.json['description']
#     author = request.json['author']

#     my_posts = Post(title, description, author)
#     db.session.add(my_posts)
#     db.session.commit()

#     return post_schema.jsonify(my_posts)




# #getting posts
# @app.route('/get', methods = ['GET'])
# def get_post():
#     all_posts = Post.query.all()
#     result = posts_schema.dump(all_posts)

#     return jsonify(result)


# #getting particular post
# @app.route('/post_details/<id>/', methods = ['GET'])
# def post_details(id):
#     post = Post.query.get(id)
#     return post_schema.jsonify(post)


# #updating post
# @app.route('/post_update/<id>/', methods = ['PUT'])
# def post_update(id):
#     post = Post.query.get(id)

#     title = request.json['title']
#     description = request.json['description']
#     author = request.json['author']


#     post.title = title
#     post.description = description
#     post.author = author

#     db.session.commit()
#     return post_schema.jsonify(post)



# #deleting post
# @app.route('/post_delete/<id>/', methods = ['DELETE'])
# def post_delete(id):
#     post = Post.query.get(id)
#     db.session.delete(post)
#     db.session.commit()

#     return post_schema.jsonify(post)




# if __name__ == "__main__":
#     app.run(debug=True)