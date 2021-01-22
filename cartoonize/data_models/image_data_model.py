
class ImageDataModel(object):
    def __init__(self, storage):
        self._storage = storage

    def find_one(self, image_id):
        return self._storage.find_one(image_id)

    def insert_one(self, image_file, file_name):
        return self._storage.insert_one(image_file, file_name)

    def find_all(self):
        return self._storage.find_all()
