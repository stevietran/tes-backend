from time import sleep
from celery import Celery
import os

from app.schemas.user_input import M_JOB

app = Celery(__name__)

app.conf.broker_url = os.environ.get("CELERY_BROKER_URL", "redis://localhost:6379/0")
app.conf.result_backend = os.environ.get("CELERY_RESULT_BACKEND", "redis://localhost:6379/0")

def send_celery(case_id):
    print(f"The case id: {case_id}")
    sleep(6)
    kwargs = {'job_data': M_JOB}
    
    res = app.send_task(name="opt_snt", kwargs=kwargs)
    id = res.task_id
    return id
