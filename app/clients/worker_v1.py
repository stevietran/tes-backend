from time import sleep
from celery import Celery
import os

from app.schemas.user_input import M_JOB

app = Celery(__name__)

app.conf.broker_url = os.environ.get("CELERY_BROKER_URL", "redis://localhost:6379/0")
app.conf.result_backend = os.environ.get("CELERY_RESULT_BACKEND", "redis://localhost:6379/0")

def send_celery(case_id, q_name):
    kwargs = {'case_id': case_id}
    
    res = app.send_task(name=q_name, kwargs=kwargs)
    id = res.task_id
    
    return id
