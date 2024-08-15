import multiprocessing
import os

# Define the path to your Django project
django_project_path = '/var/www/neurovart'  # Update with your actual project path

# Gunicorn configuration
bind = '93.127.195.182:8000'  # IP and port where Gunicorn will listen
workers = multiprocessing.cpu_count() * 2 + 1  # Number of Gunicorn worker processes
timeout = 60  # Timeout for handling requests
keepalive = 2  # Number of seconds to keep connections open
errorlog = os.path.join(django_project_path, 'gunicorn_error.log')  # Path to error log file
accesslog = os.path.join(django_project_path, 'gunicorn_access.log')  # Path to access log file
loglevel = 'info'  # Log level

# Django specific settings for Gunicorn
pythonpath = django_project_path
django_settings_module = 'neurovart.settings'  # Replace 'neurovart' with your actual Django settings module

# Handling static files
def on_starting(server):
    server.log.info("Starting Gunicorn...")
    server.log.info("Collecting static files...")
    os.system("python manage.py collectstatic --noinput")

# Preloading the application to avoid delays on first request
preload_app = True
