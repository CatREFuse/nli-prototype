import time

class AppState:
    def __init__(self) -> None:
        self.reset()

    def reset(self):
        self.subject_id = 0
        self.task_index = 0  # 0 means not start
        self.task_class = 0  # 0 os task, 1 figma task
        self.start_time = time.time()

if __name__ == "__main__":
    print(time.time())
    print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))