from time import sleep
from queue import Queue, SimpleQueue

from PySide2.QtCore import QRunnable, QThreadPool, Slot
from PySide2.QtWidgets import QLabel

class GUIThreadingManager:
    def __init__(self, thread_pool = QThreadPool) -> None:
        self.thread_pool = thread_pool

        self.led_screen = None
        self.current_led_screen_task: LEDScreenScrollTask = None
        self.led_screen_tasks = SimpleQueue()

    def register_led_screen(self, led_screen: QLabel) -> None:
        self.led_screen = led_screen

    def set_current_led_screen_task(self, text_to_scroll: str, duration: int = -1):
        self.current_led_screen_task = LEDScreenScrollTask(self.led_screen, text_to_scroll, duration)
        self.thread_pool.start(self.current_led_screen_task)

    def stop_current_led_screen_task(self):
        if self.current_led_screen_task is not None:
            self.current_led_screen_task.kill()


class LEDScreenScrollTask(QRunnable):
    def __init__(self, led_screen: QLabel, text_to_scroll: str, duration: int = -1) -> None:
        super().__init__()

        self.duration = duration

        self.time_between_updates = 0.5
        self.led_screen = led_screen
        self.text_to_scroll = text_to_scroll
        self.text_to_display = text_to_scroll

        self.current_text_offset = 0

        self.is_killed = False

    @Slot()
    def run(self):
        if self.duration <= 0:
            while True:
                if self.is_killed:
                    return
                self.single_loop()

        else:
            times_to_cycle = int(self.duration / self.time_between_updates)

            for i in range(0, times_to_cycle):
                if self.is_killed:
                    return
                self.single_loop()
            self.is_killed = True
    
    def single_loop(self):
        self.scroll_text()
        sleep(self.time_between_updates)

    def scroll_text(self) -> None:
        led_length = self.led_screen.config.led_screen_width
        text_length = len(self.text_to_scroll)

        if self.current_text_offset >= 0 and self.current_text_offset <= text_length:
            self.text_to_display.strip()
            if self.current_text_offset != 0:
                self.text_to_display = self.text_to_scroll[self.current_text_offset:]
        else:
            if self.current_text_offset > text_length:
                self.current_text_offset = (-1) * led_length
            self.text_to_display = self.led_screen.get_empty_string_for_led_width()[:abs(self.current_text_offset)-1] + self.text_to_scroll

        if len(self.text_to_display) > led_length:
            self.text_to_display = self.text_to_display[:led_length]
        
        self.current_text_offset += 1
        self.led_screen.setText(self.text_to_display)
        self.led_screen.update()

    def kill(self) -> None:
        self.is_killed = True