# Use the official Python image from the Docker Hub
FROM python:3.12.11-alpine3.22

# Set the working directory in the container
WORKDIR /code

# Copy the current directory contents into the container at /code
COPY . /code

# Install the API's own dependencies (fastapi/uvicorn to serve it), then the
# toolkit itself from local source (not PyPI -- this image should always
# reflect the code sitting next to this Dockerfile, not a published release).
RUN pip install --no-cache-dir --upgrade -r /code/toolkit/API/requirements.txt \
    && pip install --no-cache-dir --upgrade .

# Keep in sync with ./VERSION by hand when bumping the image version.
LABEL org.opencontainers.image.version="2.0.0" \
      org.opencontainers.image.source="https://github.com/wilkinsonlab/CARE-Semantic-Model-Version-2/tree/main/implementation/Toolkit"

# Command to run the application
CMD ["uvicorn", "--host", "0.0.0.0", "toolkit.API.main:app"]
