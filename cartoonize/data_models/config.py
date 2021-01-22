import os

from cartoonize.data_models.image_data_model import ImageDataModel
from cartoonize.data_models.storage.image_local_storage import ImageLocalStorage

IMAGE_DIR = os.environ.get('CARTOONIZE_IMAGE_DIR', '/Users/jamesfallon/cartoonize/images/')
image_local_storage = ImageLocalStorage(IMAGE_DIR)
image_data_model = ImageDataModel(image_local_storage)
