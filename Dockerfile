# Using the base python image
FROM python:3.7.9

WORKDIR /code

# Install requirements
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy source code over
COPY cartoonize/ /code/cartoonize
COPY setup.py /code/

# Install our cartoonize package
RUN python setup.py install

# Set directory for image uploads
ENV CARTOONIZE_IMAGE_DIR=/images
RUN mkdir /images

# Run the flask app
ENTRYPOINT ["python"]
CMD ["cartoonize/app.py"]