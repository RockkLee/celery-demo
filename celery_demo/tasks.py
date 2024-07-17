import time
from celery import Celery


celery = Celery('tasks', broker='pyamqp://username:password@localhost//')
celery.conf.update(
    task_serializer='json'
)


@celery.task
def demo_task(demo_str: str, demo_int: int, demo_float: float) -> str:
    time.sleep(10)
    print(f'demo_task: str:{demo_str} int:{demo_int} float:{demo_float}')
    return 'demo_task_success'


@celery.task
def demo_task2(demo_str: str, demo_int: int, demo_float: float) -> str:
    print(f'demo_task2: str:{demo_str} int:{demo_int} float:{demo_float}')
    return 'demo_task2_success'


# create celery workers
# Linux: celery -A <module-name> worker --loglevel=info --concurrency=<number of workers>
# Windows: celery -A <module-name> worker --loglevel=info -P eventlet --concurrency=<number of workers>
