from flask import Flask
from flask_restful import Api
from cartoonize.apis.image import ImageList, Image
from cartoonize.apis.cartoonize import Cartoonize

app = Flask(__name__)
api = Api(app)

api.add_resource(ImageList, '/images')
api.add_resource(Image, '/images/<image_id>')
api.add_resource(Cartoonize, '/images/<image_id>/cartoonize')

if __name__ == '__main__':
    app.run(host='0.0.0.0')
