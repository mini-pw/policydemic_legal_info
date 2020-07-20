import os

if os.environ.get('RUNNING_IN_DOCKER', False):
    broker_url = "amqp://guest:guest@rabbitmq:5672//"
else:
    broker_url = "pyamqp://"
result_backend = "rpc://"

task_serializer = "json"
result_serializer = "json"
accept_content = ["json"]
timezone = "Europe/Warsaw"
enable_utc = True
imports = (
    "scheduler.tasks",
    "crawler.tasks",
    "nlpengine.tasks",
    "pdfparser.tasks",
    "translator.tasks",
)
