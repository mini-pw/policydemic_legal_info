from scheduler.celery import app


@app.task
def pdfparser():
    print("Hello queue world!")
