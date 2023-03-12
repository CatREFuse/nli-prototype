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
    return 'M-CAT'


@app.route('/reset')
def reset():
    state.reset()
    return "ok"


@app.route('/set-subject-id/<int:subject_id>', methods=["POST", "OPTION"])
def set_subject_id(subject_id):
    state.reset()
    state.subject_id = subject_id
    return "ok"


@app.route('/state')
def get_state():
    state_dict = {
        "subject_id": state.subject_id,
        "state": state.state,
        "task_round": state.task_round,
        "task_class": state.task_class,
        "task_index": state.task_index,
        "mouse_distance": key_logger.mouse_distance,
        "mouse_click": key_logger.mouse_click,
        "keyborad_press": key_logger.keyboard_press,
        "start_time": state.start_time,
        "data_buffer": state.data_buffer,
        "prompt": state.prompt
    }
    print(state_dict)
    return json.dumps(state_dict)


@app.route("/start/<int:task_round>/<int:task_class>")
def start(task_round: int, task_class: int):
    state.task_index = 0
    state.state = 1
    state.task_round = task_round
    state.task_class = task_class
    state.start_time = round(time.time(), 3)
    return "ok"


@app.route("/prompt/<string:prompt>")
def set_prompt(prompt):
    state.prompt = prompt
    print(f"get prompt: {prompt} ")
    return "ok"


@app.route("/begin-task")
def begin_task():
    state.prompt = ""
    state.state = 2
    key_logger.reset()
    state.start_time = round(time.time(), 3)
    return "ok"

@app.route("/repeat")
def repeat():
    # 记录数据
    end_time = round(time.time(), 3)
    state.data_buffer.append([state.subject_id, state.task_round, state.task_class, state.task_index, key_logger.mouse_distance,
                              key_logger.mouse_click, key_logger.keyboard_press, 0, state.start_time, end_time, state.prompt])
    state.state = 1
    return "ok"


@app.route("/next")
def next():
    # 记录数据
    end_time = round(time.time(), 3)

    state.data_buffer.append([state.subject_id, state.task_round, state.task_class, state.task_index, key_logger.mouse_distance,
                              key_logger.mouse_click, key_logger.keyboard_press, 1, state.start_time, end_time, state.prompt])

    if state.task_index == 5:
        for item in state.data_buffer:
            item = [i for i in item]
            append_log(*item)

        if state.task_round == 1 and state.task_class == 1:
            reset()
        else:
            id = state.subject_id
            reset()
            state.subject_id = id

        return "end"
    else:
        state.task_index += 1
        state.state = 1
        return "next"


def append_log(subject_id, task_round, task_class, task_index, mouse_distance, mouse_click, keyboard_press, success, start_time, end_time, prompt):
    duration = round(end_time - start_time, 3)
    with open("log.csv", "a") as log:
        log.write("{0},{1},{2},{3},{4},{5},{6},{7},{8},{9},{10},{11}\n".format(subject_id, task_round, task_class,
                  task_index, mouse_distance, mouse_click, keyboard_press, success, start_time, end_time, duration, prompt))
    return "append success"


@app.route("/static/:filename")
def static_file(filename):
    return app.send_static_file(filename)
