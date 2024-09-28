FROM python:3.11-bookworm

ENV PYTHONUNBUFFERED=1 \
    DJANGO_SETTINGS_MODULE=storefront.settings.prod

# Set the working directory
WORKDIR /django

# Update pip first
RUN pip install --upgrade pip

# Copy the requirements file and install dependencies
COPY requirements.txt /django/requirements.txt
RUN pip3 install -r requirements.txt

# Copy the project files
COPY . .

# Make port 8000 available to the world outside this container
CMD gunicorn storefront.wsgi:application --bind 0.0.0.0:8000

EXPOSE 8000