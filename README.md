# cartoonize

## About

This is a Flask API which allows users to upload, download and 'cartoonize' image files.

## Installation / Running the API

### Option 1: Run it locally

    pip install -r requirements.txt
    python setup.py install
    python cartoonize/app.py

### Option 2: Run it as a Docker image

    docker build -t cartoonize .
    docker run -d -p 5000:5000 cartoonize


# Testing

## Run Unit Tests
    pip install pytest
    python -m pytest

## API Endpoints
`GET /images` 

Returns the list of images currently stored on the server.

    curl http://0.0.0.0:5000/images
    

Upload an image.

    curl -v -F "image=@/Users/jamesfallon/Pictures/some-photo.jpg" http://0.0.0.0:5000/images

`GET /images/<image_id>` 

Download the image with id <image_id>.

    curl http://0.0.0.0:5000/images/<image_id> --output ./image.jpg

`GET /images/<image_id>/cartoonize` 

Download a cartoonified version of an image.

    curl http://0.0.0.0:5000/images/<image_id>/cartoonize --output ./cartoonified_image.jpg
