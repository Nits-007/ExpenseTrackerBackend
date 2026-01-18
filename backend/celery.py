import os
from celery import Celery
from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.abspath(__file__))  
load_dotenv(os.path.join(BASE_DIR, "..", ".env"))  

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

app = Celery('backend')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()