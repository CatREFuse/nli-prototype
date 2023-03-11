from pynput import keyboard
from pynput import mouse
import pyautogui
import math


class KeyLogger:

    def __init__(self) -> None:
        self.reset()

    def reset(self):
        self.keyboard_press = 0
        self.mouse_click = 0
        self.mouse_position = [0, 0]
        self.mouse_distance = 0
        print("keylogger 初始化完成")

    def begin(self):

        self.mouse_position = [pyautogui.position().x, pyautogui.position().y]

        def on_press(key):
            self.keyboard_press += 1
            # print('keyboard press: ', self.keyboard_press)

        def on_release(key):
            pass

        def on_click(x, y, button, pressed):
            if pressed:
                self.mouse_click += 1
                # print('mouse click: ', self.mouse_click)

        def on_scroll(x, y, dx, dy):
            pass

        def on_move(x, y):
            # print('Mouse moved to ({0}, {1})'.format(x, y))
            self.mouse_distance += math.sqrt(
                (x - self.mouse_position[0]) ** 2 + (y - self.mouse_position[1]) ** 2)
            self.mouse_distance = int(self.mouse_distance)
            self.mouse_position = [x, y]

        with keyboard.Listener(on_press=on_press, on_release=on_release) as listener1, mouse.Listener(on_click=on_click, on_scroll=on_scroll, on_move=on_move) as listener2:
            listener1.join()
            listener2.join()


if __name__ == "__main__":
    key_logger = KeyLogger()
    key_logger.begin()
