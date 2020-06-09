from scheduler.celery import app


@app.task
def hello_world():
    print("Hello queue world!")
