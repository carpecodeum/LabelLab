import os
import sys
import base64
from io import BytesIO
from PIL import Image as image_pil
from werkzeug.utils import secure_filename

from api.config import config
from api.extensions import db, ma
from api.models.Image import Image
from api.serializers.image import ImageSchema

image_schema = ImageSchema()
images_schema = ImageSchema(many=True)

def to_json(Image):
    """
    Returns a Image JSON object
    """
    return image_schema.dump(Image).data

def find_by_id(_id):
    """
    query Image on their id
    """
    image = Image.query.filter_by(id=_id).first()
    return image_schema.dump(image).data

def find_by_image_name(image_name):
    """
    query Image on their Imagename
    """
    image = Image.query.filter_by(image_name=image_name).first()
    return image_schema.dump(image).data

def find_all_by_project_id(project_id):
    """
    query images based on their project_id.
    """
    images = Image.query.filter_by(project_id=project_id).all()
    return images_schema.dump(images).data

def remove_image(image_id):
    image = find_by_id(image_id)
    project_id = image['project_id']
    image_url = image['image_url']
    parent_dir = config['development'].UPLOAD_FOLDER
    directory = f"{project_id}/{image_url}"
    path = os.path.join(parent_dir, directory)
    try:
        os.remove(path)
        return path
    except Exception as err:
        return f"Error occured: {err}"

def delete_by_id(_id):
    """
    Delete Image by their id
    """
    Image.query.filter_by(id=_id).delete()
    db.session.commit()
    
def delete_by_image_name(image_name):
    """
    Delete Image by their name
    """
    Image.query.filter_by(image_name=image_name).delete()
    db.session.commit()

def get_dimensions(file):
    """
    get dimensions of an image
    """
    starter = file.find(',')
    image_data = file[starter+1:]
    image_data = bytes(image_data, encoding="ascii")
    image = image_pil.open(BytesIO(base64.b64decode(image_data)))
    width, height = image.size
    return {
        "height": height,
        "width": width
    }

def convert_and_save(file, project_id, image_url):
    """
    convert the base64 string to image and then save it
    """
    starter = file.find(',')
    image_data = file[starter+1:]
    image_data = bytes(image_data, encoding="ascii")
    image = image_pil.open(BytesIO(base64.b64decode(image_data)))
    parent_dir = config['development'].UPLOAD_FOLDER
    directory = f"{project_id}"
    dir_path = os.path.join(parent_dir, directory)
    try: 
        os.makedirs(dir_path, exist_ok = True)
    except OSError as error: 
        return f"Error occured: {error}"
    path = os.path.join(dir_path,f"{image_url}")
    try:
        image.save(path)
        return path
    except Exception as err:
        return f"Error occured: {err}"

def save(image):
    """
    Save a Image to the database.
    This includes creating a new Image and editing one.
    """
    db.session.add(image)
    db.session.commit()
    return image_schema.dump(image).data
