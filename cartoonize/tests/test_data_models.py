import unittest
from unittest.mock import Mock
from cartoonize.data_models.image_data_model import ImageDataModel


class TestImageDataModel(unittest.TestCase):
    def setUp(self):
        self.storage_mock = Mock()

    def test_find_one_success(self):
        fake_image_path = '/fake/image.png'
        self.storage_mock.configure_mock(**{
            'find_one.return_value': fake_image_path
        })
        data_model = ImageDataModel(self.storage_mock)

        item = data_model.find_one('image_id_1')

        self.assertEqual(item, fake_image_path)
        self.storage_mock.find_one.assert_called()

    def test_insert_one_success(self):
        self.storage_mock = Mock()
        self.storage_mock.configure_mock(**{
            'insert_one.return_value': 'dc4e52ee-6bdb-4b26-8c4f-fa6b5fbf152a'
        })
        data_model = ImageDataModel(self.storage_mock)
        fake_image = Mock()
        fake_path = '/fake/image.png'
        result = data_model.insert_one(fake_image, fake_path)

        self.assertEqual(result, 'dc4e52ee-6bdb-4b26-8c4f-fa6b5fbf152a')
        self.storage_mock.insert_one.assert_called_with(fake_image, fake_path)

    def test_find_all_success(self):
        self.storage_mock = Mock()
        self.storage_mock.configure_mock(**{
            'find_all.return_value': {
                '123': 'image.png',
                'abc': 'photo.jpg'
            }
        })
        data_model = ImageDataModel(self.storage_mock)
        result = data_model.find_all()

        self.assertEqual(result, {
                '123': 'image.png',
                'abc': 'photo.jpg'
            })
        self.storage_mock.find_all.assert_called()
