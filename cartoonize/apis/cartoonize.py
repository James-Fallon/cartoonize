import os

import cv2
from flask import send_file
from flask_restful import Resource, abort

from cartoonize.data_models.config import image_data_model


class Cartoonize(Resource):

    def get(self, image_id):
        image_path = image_data_model.find_one(image_id)
        if image_path is None:
            abort(404, message=f"Image with the id '{image_id}' doesn't exist")
        cartoon_image_path = self._cartoonize_image(image_path)
        return send_file(cartoon_image_path)

    @staticmethod
    def _cartoonize_image(image_path):
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
            # TODO - Need a better way to keep track of already cartoonified images
            return cartoon_image_path

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

        return cartoon_image_path
