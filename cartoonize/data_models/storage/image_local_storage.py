import os
from uuid import uuid4


class ImageLocalStorage(object):
    def __init__(self, folder_path):
        self.folder_path = folder_path
        self.images_dict = {}

    def find_one(self, image_id):
        result = self.images_dict.get(image_id)
        if result is None:
            return None
        path = os.path.join(self.folder_path, result)
        return path

    def find_all(self):
        return self.images_dict

    def insert_one(self, image_file, file_name):
        image_id = str(uuid4())
        self.images_dict[image_id] = file_name
        image_file.save(os.path.join(self.folder_path, file_name))
        return image_id
