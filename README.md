# policydemic_legal_info

infrastracture to gather database of legal documents, and legal information gathered regarding legal changes in society during pandemy in 2020

## Setup for development
In main project directory run:
```
poetry install
```
This will install all required packages. Run `potery add package` or `poetry add package --dev` to add additional packages to use in python modules.

Backend and Frontend use yarn package manager. Install dependencies with:
```
yarn install
```
To install additional packages run `yarn add package` or `yarn add package --dev`.

### RabbitMQ
The easiest setup for RabbitMQ is to run it in docker:
```
docker run -d -p 5672:5672 rabbitmq
```
Otherwise refer to RabbitMQ documentation for installing and configuring an instance

## Celery
Comunnication and task scheduling is handled by Celery. Celery application is defined and configured in scheduler module.
Define tasks in module.tasks otherwise update imports config in scheduler.celeryconfig

Documentation:

***https://docs.celeryproject.org/en/stable/getting-started/next-steps.html#using-celery-in-your-application***

### Staring workers
Starting regular queue worker:
```
celery -A scheduler worker -l info
```
Starting beat service for periodic tasks:
```
celery -A scheduler beat
```
Test your queues by running modifing and running `python cli.py`.

## Packages

- backend - node.js+koa server
- frontend - create-react-app frontend SPA
- scheduler - celery configuration and scheduling tasks
- crawler - website crawling code and celery task definitions (LAD, SSD)
- nlpengine - processing of crawled files and input to DB
- translator - translating db records and documents
- pdfparser - parsing and filtering documents

## Deployment
There are 2 options to start the services:
* docker-compose (recommended) - run `docker-compose up --build`, which will start 2 containers: one with the `rabbitmq` service and another one with celery scheduler, based on image defined in `Dockerfile`.
* pure Docker - run each container individually.

In order to build the docker image of policydemic, run: `docker build -t minipw/policydemic:latest .`.
Then, it can be started with: `docker run minipw/policydemic:latest`.
