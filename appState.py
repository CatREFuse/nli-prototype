import time


class AppState:
    def __init__(self) -> None:
        self.reset()

    def reset(self):
        self.state = 0  # 0: 没开始 1: 等待读说明 2: 进行中
        self.subject_id = 0  # 被试 id, 0 代表没配置被试
        self.task_round = 0  # 0: WIMP轮  1: M-CAT轮
        self.task_class = 0  # 0: macOS任务集  1:Figma任务集
        self.task_index = 0  # 任务 index, 0 代表没开始
        self.start_time = time.time()
        self.prompt = ""
        self.data_buffer = []


if __name__ == "__main__":
    print(time.time())
    print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
