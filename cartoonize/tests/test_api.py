import json
import os
import unittest
from shutil import copyfile
from unittest import mock

from werkzeug.datastructures import FileStorage

from cartoonize.api import app, IMAGE_DIR

SAMPLE_IMAGE_PATH = os.path.join(os.path.dirname(__file__), 'resources', 'winnie.jpg')


class TestCartoonizeAPI(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()

    def test_get_images(self):
        fake_image_list = {
            "123": "test_image.jpg",
            "345": "other_sample_image.png"
        }

        with mock.patch.dict('cartoonize.image.IMAGES', fake_image_list):
            resp = self.client.get('/images')

        images_data = json.loads(resp.data)
        self.assertEqual(images_data, fake_image_list)

    def test_post_image(self):

        test_image_file = FileStorage(
            stream=open(SAMPLE_IMAGE_PATH, "rb"),
            filename="winnie.jpg"
        ),

        self.client.post(
            "/images",
            data={
                "image": test_image_file,
            },
            content_type="multipart/form-data"
        )

        # assert that the file saved correctly in the upload folder
        self.assertTrue(os.path.exists(os.path.join(IMAGE_DIR, 'winnie.jpg')))

        # cleanup
        os.remove(os.path.join(IMAGE_DIR, 'winnie.jpg'))

    def test_post_image_invalid_file_type(self):
        invalid_image_file = FileStorage(
            stream=open(SAMPLE_IMAGE_PATH, "rb"),
            filename="winnie.csv"
        ),

        resp = self.client.post(
            "/images",
            data={
                "image": invalid_image_file,
            },
            content_type="multipart/form-data"
        )

        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.json, {
            'message': "File 'winnie.csv' is not a valid image file."
        })

    def test_get_image(self):
        # Manually move our test image to the upload folder
        copyfile(SAMPLE_IMAGE_PATH, os.path.join(IMAGE_DIR, 'winnie.jpg'))

        fake_image_list = {
            "123": "winnie.jpg"
        }

        with mock.patch.dict('cartoonize.image.IMAGES', fake_image_list):
            resp = self.client.get('/images/123')

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.mimetype, 'image/jpeg')

        # cleanup
        os.remove(os.path.join(IMAGE_DIR, 'winnie.jpg'))