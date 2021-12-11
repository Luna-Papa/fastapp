from celery import Celery

app = Celery('FastApp')
app.config_from_object('celery_app.celeryconfig')
app.autodiscover_tasks(['celery_app'])


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
