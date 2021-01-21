import os
from uuid import uuid4

from flask import send_from_directory, redirect
from flask_restful import Resource, abort, reqparse
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename

# Crude storage for now
IMAGES = {
    '123': 'winnie.jpg'
}
VALID_IMG_EXTENSIONS = ('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif')


def abort_if_image_id_not_found(image_id):
    if image_id not in IMAGES:
        abort(404, message=f"Image with the id '{image_id}' doesn't exist")


class Cartoonize(Resource):

    def get(self, image_id):
        abort_if_image_id_not_found(image_id)
        # TODO - cartoonize the image
        return IMAGES[image_id]


class Image(Resource):
    def __init__(self, **kwargs):
        self.image_folder = kwargs['image_folder']

    def get(self, image_id):
        abort_if_image_id_not_found(image_id)
        filename = IMAGES[image_id]
        return send_from_directory(self.image_folder, filename)


class ImageList(Resource):
    def __init__(self, **kwargs):
        self.image_folder = kwargs['image_folder']

    def get(self):
        return IMAGES

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('image', type=FileStorage, location='files')
        args = parser.parse_args()
        image_file = args['image']

        if image_file.filename.lower().endswith(VALID_IMG_EXTENSIONS) is False:
            abort(400, message=f"File '{image_file.filename}' is not a valid image file.")

        filename = secure_filename(image_file.filename)
        image_file.save(os.path.join(self.image_folder, filename))
        image_id = str(uuid4())
        IMAGES[image_id] = filename
        return redirect(f'/images/{image_id}')
