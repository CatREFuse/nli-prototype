import time
from flask import Flask, request
import flask_cors
import json
from listen import KeyLogger
from appState import AppState
import threading

app = Flask(__name__)

flask_cors.CORS(app)


def key_logger_worker():
    global key_logger
    key_logger = KeyLogger()
    key_logger.begin()


key_logger_thread = threading.Thread(target=key_logger_worker)
key_logger_thread.start()

state = AppState()


@app.route('/')
def index():
    return f'被试 ID: {state.subject_id}, 实验序号: {state.task_index}, 距离: {key_logger.mouse_distance}, 点击: {key_logger.mouse_click}, 按键: {key_logger.keyboard_press}'


@app.route('/api/reset')
def reset():
    state.reset()
    key_logger.reset()


@app.route('/api/state')
def get_state():
    state_dict = {
        "subject_id": state.subject_id,
        "task_index": state.task_index,
        "task_class": state.task_class,
        "mouse_distance": key_logger.mouse_distance,
        "mouse_click": key_logger.mouse_click,
        "keyborad_press": key_logger.keyboard_press,
        "start_time": state.start_time,
    }
    return json.dumps(state_dict)


@app.route("/api/start/int:task_class")
def start(task_class: int):
    key_logger.reset()
    state.task_index = 1
    state.task_class = task_class
    state.start_time = time.time()
    return 200


@app.route("/api/next")
def next():
    # 记录数据
    end_time = time.time()
    append_log(state.subject_id, state.task_class, state.task_index, key_logger.mouse_distance,
               key_logger.mouse_click, key_logger.keyboard_press, 1, state.start_time, end_time)

    # 状态更改: index + 1; 结束实验; 清除按键
    key_logger.reset()
    state.start_time = time.time()
    if state.task_index == 6:
        reset()
        return "end"
    else:
        state.task_index += 1


@app.route("/api/repeat")
def repeat():
    # 记录数据
    end_time = time.time()
    append_log(state.subject_id, state.task_class, state.task_index, key_logger.mouse_distance,
               key_logger.mouse_click, key_logger.keyboard_press, 0, state.start_time, end_time)
    key_logger.reset()
    state.start_time = time.time()
    return 200


def append_log(subject_id, task_class, task_index, mouse_distance, mouse_click, keyboard_press, success, start_time, end_time):
    duration = end_time - start_time
    with open("log.csv", "a") as log:
        log.write("{0},{1},{2},{3},{4},{5},{6},{7},{8},{9},{10}\n".format(subject_id, task_class,
                  task_index, mouse_distance, mouse_click, keyboard_press, success, start_time, end_time, duration))
    return "append success"


@app.route("/static/:filename")
def static_file(filename):
    return app.send_static_file(filename)
