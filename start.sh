# gunicorn -w 4 -k uvicorn.workers.UvicornWorker app:app
gunicorn --worker-class uvicorn.workers.UvicornWorker --timeout 600 --access-logfile '-' --error-logfile '-' app:app