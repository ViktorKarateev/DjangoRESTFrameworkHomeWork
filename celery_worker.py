import eventlet
eventlet.monkey_patch()

from config.celery import app

app.worker_main()
