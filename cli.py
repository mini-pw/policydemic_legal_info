# Helper file for testing queues
from crawler.tasks import hello_world

hello_world.delay()
print("Done!")
