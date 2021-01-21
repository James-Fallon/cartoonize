import os
from uuid import uuid4
import cv2
from flask import send_from_directory, redirect
from flask_restful import Resource, abort, reqparse
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename

# Crude storage for now
IMAGES = {}
VALID_IMG_EXTENSIONS = ('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif')


def abort_if_image_id_not_found(image_id):
    if image_id not in IMAGES:
        abort(404, message=f"Image with the id '{image_id}' doesn't exist")


def cartoonize(image_path):
    """

    The idea here to 'cartoonize' an image has 2 steps.
    1. Find the edges and accentuate them.
    2. Smooth out the colours in the rest of image.

    :param image_path:
    :return:
    """
    original_image_name, file_ext = os.path.splitext(os.path.basename(image_path))
    cartoon_image_name = f'{original_image_name}_cartoonified{file_ext}'
    cartoon_image_path = os.path.join(os.path.dirname(image_path), cartoon_image_name)

    if os.path.exists(cartoon_image_path):
        # We've already cartoonified this one before
        return cartoon_image_name

    original_image = cv2.imread(image_path)
    original_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB)

    # 1. Find the edges
    # We convert the image to grayscale and smooth it. Find the edges using adaptive thresholding
    grayscale_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)
    smooth_grayscale_image = cv2.medianBlur(grayscale_image, 5)
    edges = cv2.adaptiveThreshold(smooth_grayscale_image, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 9)

    # 2. Apply bilateral filtering to remove noise and smooth out the colours
    color_image = cv2.bilateralFilter(original_image, 9, 300, 300)

    # Join the smoothed out image with the sharp edges to give a cartoon effect
    cartoon_image = cv2.bitwise_and(color_image, color_image, mask=edges)

    # Save the file
    cv2.imwrite(cartoon_image_path, cv2.cvtColor(cartoon_image, cv2.COLOR_RGB2BGR))

    return cartoon_image_name


class Cartoonize(Resource):
    def __init__(self, **kwargs):
        self.image_folder = kwargs['image_folder']

    def get(self, image_id):
        abort_if_image_id_not_found(image_id)
        cartoonified_image_name = cartoonize(os.path.join(self.image_folder, IMAGES[image_id]))
        return send_from_directory(self.image_folder, cartoonified_image_name)


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


if __name__ == '__main__':
    cartoonify('/Users/jamesfallon/cartoonize/cartoonize/tests/resources/the-mandalorian.jpg')
