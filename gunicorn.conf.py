import os

bind = f"0.0.0.0:{os.environ.get('PORT', '8080')}"
workers = int(os.environ.get("GUNICORN_WORKERS", "2"))   # procesos
threads = int(os.environ.get("GUNICORN_THREADS", "4"))   # hilos por proceso
worker_class = "gthread"                                  # worker con hilos
timeout = 30                                              # segundos antes de reiniciar un worker colgado
accesslog = "-"                                           # logs de requests a stdout