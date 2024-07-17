from tasks import demo_task, demo_task2


if __name__ == '__main__':
    demo_task.delay('hello', 1, 2.0)
    demo_task2.delay('hello', 3, 4.0)
    print("done!!!")
