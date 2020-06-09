from __future__ import absolute_import, unicode_literals

from celery import Celery

app = Celery("scheduler")
app.config_from_object('scheduler.celeryconfig')

if __name__ == "__main__":
    app.start()
