# celery-demo
## Concept
- Celery is a asynchronous task queue
  - Although we say it is "asynchronous", each worker only has one thread and can't run asynchronously like fastapi with asyncio.
  - Therefore, if we only set up one worker for task queue, it will still be blocked by io like running code normally.
- The structure of Celery consists of one or many workers, one message broker, and clients.
- Celery can also be used as a batch app with an asynchronous task queue.

## Step1: Run the message broker
- Run the docker-compose.yml to start the message broker which is RabbitMQ for this project.

## Step2: Create Works
- Write a task model that can be run by workers.
  - tasks.py
```python
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
```

- Create workers by loading the task functions from the model we created.
```sh
celery-demo$ tree ./ -L 2
./
├── README.md
├── celery_demo
│         ├── __init__.py
│         ├── client.py
│         └── tasks.py
├── docker-compose.yml
├── poetry.lock
└── pyproject.tom
celery-demo$ cd celery_demo

# Linux
# celery -A <module-name> worker --loglevel=info --concurrency=<number of workers>
# Windows
# celery-demo$ celery -A <module-name> worker --loglevel=info -P eventlet --concurrency=<number of workers>
celery-demo$ celery -A tasks worker --loglevel=info -P eventlet --concurrency=2
```

- Grow three queues after creating the workers
  - `celery`: 
    - The queue contains the jobs that is waiting to be executed
  - `celery@MSI.celery.pidbox`
    - This is a control queue used by Celery workers for remote control commands.
  - `celeryev.2b241f7c-7294-4a3a-b895-6034095adced`
    - This is an event queue used by Celery to publish events. 
![img.png](./doc/img.png)

## Step3: Run the task functions from clients
- Run the task functions from clients to invoke the workers.
  - Run `client.py`
```python
if __name__ == '__main__':
    demo_task.delay('hello', 1, 2.0)
    demo_task2.delay('hello', 3, 4.0)
    print("done!!!")
```

- Outputs are in the shell where we entered to start the works
```sh
#  celery -A tasks worker --loglevel=info -P eventlet --concurrency=2
[2024-07-18 02:37:03,758: INFO/MainProcess] Task tasks.demo_task[2da781bc-cef4-4583-b294-800fbced2991] received
[2024-07-18 02:37:03,759: INFO/MainProcess] Task tasks.demo_task2[c8c98008-1987-4f0f-a9d4-3dcfbf731976] received
[2024-07-18 02:37:03,761: WARNING/MainProcess] demo_task2: str:hello int:3 float:4.0
[2024-07-18 02:37:03,768: INFO/MainProcess] Task tasks.demo_task2[c8c98008-1987-4f0f-a9d4-3dcfbf731976] succeeded in 0.0s: 'demo_task2_success'
[2024-07-18 02:37:13,760: WARNING/MainProcess] demo_task: str:hello int:1 float:2.0
[2024-07-18 02:37:13,765: INFO/MainProcess] Task tasks.demo_task[2da781bc-cef4-4583-b294-800fbced2991] succeeded in 10.01600000000326s: 'demo_task_success'

#  celery -A tasks worker --loglevel=info -P eventlet --concurrency=1
[2024-07-18 02:38:06,610: INFO/MainProcess] Task tasks.demo_task[800ac4eb-b85a-4007-960d-e85e2341766e] received
[2024-07-18 02:38:06,611: INFO/MainProcess] Task tasks.demo_task2[38439a57-8dde-40fc-bf52-ef9b3ca5fe86] received
[2024-07-18 02:38:16,621: WARNING/MainProcess] demo_task: str:hello int:1 float:2.0
[2024-07-18 02:38:16,626: INFO/MainProcess] Task tasks.demo_task[800ac4eb-b85a-4007-960d-e85e2341766e] succeeded in 10.014999999984866s: 'demo_task_success'
[2024-07-18 02:38:16,627: WARNING/MainProcess] demo_task2: str:hello int:3 float:4.0
[2024-07-18 02:38:16,631: INFO/MainProcess] Task tasks.demo_task2[38439a57-8dde-40fc-bf52-ef9b3ca5fe86] succeeded in 0.0s: 'demo_task2_success'
```
