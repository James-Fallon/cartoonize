import json
import os
import unittest
from unittest.mock import patch

from werkzeug.datastructures import FileStorage

from cartoonize.app import app

SAMPLE_IMAGE_PATH = os.path.join(os.path.dirname(__file__), 'resources', 'the-mandalorian.jpg')


class TestCartoonizeAPI(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()

    @patch("cartoonize.apis.image.image_data_model")
    def test_get_images(self, image_data_model_mock):

        fake_image_list = {
            "123": "test_image.jpg",
            "345": "other_sample_image.png"
        }
        image_data_model_mock.find_all.return_value = fake_image_list
        resp = self.client.get('/images')

        images_data = json.loads(resp.data)
        self.assertEqual(images_data, fake_image_list)

    @patch("cartoonize.apis.image.image_data_model")
    def test_post_image(self, image_data_model_mock):
        test_image_file = FileStorage(
            stream=open(SAMPLE_IMAGE_PATH, "rb"),
            filename="the-mandalorian.jpg",
            content_type='image/jpeg',
            name='image'
        ),

        self.client.post(
            "/images",
            data={
                "image": test_image_file,
            }
        )
        actual_file_storage, actual_path = image_data_model_mock.insert_one.call_args[0]

        self.assertEqual(actual_file_storage.filename, test_image_file[0].filename)
        self.assertEqual(actual_path, "the-mandalorian.jpg")

    def test_post_image_invalid_file_type(self):
        invalid_image_file = FileStorage(
            stream=open(SAMPLE_IMAGE_PATH, "rb"),
            filename='the-mandalorian.csv'
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
            'message': "File 'the-mandalorian.csv' is not a valid image file."
        })

    @patch("cartoonize.apis.image.image_data_model")
    def test_get_image(self, image_data_model_mock):
        image_data_model_mock.find_one.return_value = SAMPLE_IMAGE_PATH

        resp = self.client.get('/images/123')

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.mimetype, 'image/jpeg')

    @patch("cartoonize.apis.cartoonize.image_data_model")
    def test_cartoonize(self, image_data_model_mock):
        image_data_model_mock.find_one.return_value = SAMPLE_IMAGE_PATH

        resp = self.client.get('/images/123/cartoonize')

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.mimetype, 'image/jpeg')
