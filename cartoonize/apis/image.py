from flask import send_file, redirect
from flask_restful import Resource, abort, reqparse
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename

from cartoonize.data_models.config import image_data_model

VALID_IMG_EXTENSIONS = ('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif')


class Image(Resource):
    def get(self, image_id):
        image_path = image_data_model.find_one(image_id)
        if image_path is None:
            abort(404, message=f"Image with the id '{image_id}' doesn't exist")
        return send_file(image_path)


class ImageList(Resource):
    def get(self):
        return image_data_model.find_all()

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('image', type=FileStorage, location='files')
        args = parser.parse_args()
        image_file = args['image']
        # Make sure the filename is safe to use
        filename = secure_filename(image_file.filename)

        if image_file.filename.lower().endswith(VALID_IMG_EXTENSIONS) is False:
            abort(400, message=f"File '{image_file.filename}' is not a valid image file.")

        for existing_image_name in image_data_model.find_all().values():
            if existing_image_name.lower() == filename.lower():
                abort(409, message=f'Image name "{filename}" already in use.')

        image_id = image_data_model.insert_one(image_file, filename)

        return redirect(f'/images/{image_id}')
