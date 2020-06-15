# from scheduler.celery import app
# from pdfparser.tasks import pdfparser


# @app.task
# def scan_website(link):
#     html = curl(link)
#     parsedhtml = parse(html)
#     # TODO get links from html
#     # add links to crawl QUEUE
#     for scrapped_link in scrapped_links:
#         scan_website.delay(scrapped_link)


# @app.task
# def crawl():
#     # TODO list of gov links
#     for link in gov_links:
#         if pdf:
#             pdfparser.delay(pdf)
#         else:
#             scan_website.delay(link)

#     print("Hello queue world!")
