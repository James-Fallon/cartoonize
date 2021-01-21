import os

from flask import Flask
from flask_restful import Api

from cartoonize.image import ImageList, Image, Cartoonize

IMAGE_DIR = os.environ.get('CARTOONIZE_IMAGE_DIR', '/Users/jamesfallon/cartoonize/images/')
if os.path.exists(IMAGE_DIR) is False:
    os.mkdir(IMAGE_DIR)

app = Flask(__name__)
api = Api(app)

api.add_resource(ImageList, '/images', resource_class_kwargs={'image_folder': IMAGE_DIR})
api.add_resource(Image, '/images/<image_id>', resource_class_kwargs={'image_folder': IMAGE_DIR})
api.add_resource(Cartoonize, '/images/<image_id>/cartoonize')

if __name__ == '__main__':
    app.run(host='0.0.0.0')
