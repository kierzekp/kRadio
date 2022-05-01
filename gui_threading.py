from time import sleep
from queue import Queue

from PySide2.QtCore import QRunnable, QThreadPool, Slot
from PySide2.QtWidgets import QLabel

class GUIThreadingManager:
    def __init__(self, thread_pool = QThreadPool) -> None:
        self.thread_pool = thread_pool
        self.task_queue_manager = TaskQueueManager(self)

        self.led_screen = None
        self.current_led_screen_task: LEDScreenScrollTask = None
        self.led_screen_tasks = Queue()

        self.thread_pool.start(self.task_queue_manager)

    def register_led_screen(self, led_screen: QLabel) -> None:
        self.led_screen = led_screen

    def add_led_screen_task_to_queue(self, text_to_scroll: str, duration: int = -1):
        task_desc = {"text_to_scroll": text_to_scroll, "duration": duration}
        self.led_screen_tasks.put(task_desc)

    def display_preset_change(self, preset_name: str):
        if self.task_queue_manager is not None:
            self.stop_current_led_screen_task()
            self.task_queue_manager.clear_queue()
            sleep(0.1)
            self.add_led_screen_task_to_queue(preset_name)

    def set_current_led_screen_task(self, task_desc: dict):
        self.current_led_screen_task = LEDScreenScrollTask(self.led_screen, task_desc)
        self.thread_pool.start(self.current_led_screen_task)

    def stop_current_led_screen_task(self):
        if self.current_led_screen_task is not None:
            self.current_led_screen_task.kill()

    def kill_running_threads(self):
        if self.task_queue_manager is not None:
            self.task_queue_manager.clear_queue()
            self.task_queue_manager.kill()
        if self.current_led_screen_task is not None:
            self.current_led_screen_task.kill()
        

class TaskQueueManager(QRunnable):
    def __init__(self, gui_threading_manager: GUIThreadingManager) -> None:
        super().__init__()
        self.gtm = gui_threading_manager

        self.is_killed = False
        self.to_clear_queue = False

    @Slot()
    def run(self):
        while True:
            if self.is_killed:
                return
            if self.to_clear_queue:
                while not self.gtm.led_screen_tasks.empty():
                    self.gtm.led_screen_tasks.get()
                self.to_clear_queue = False
            self.process_queue()
            sleep(0.1)

    def process_queue(self):
        if not self.gtm.led_screen_tasks.empty():
            if self.gtm.current_led_screen_task is None or self.gtm.current_led_screen_task.is_killed:
                self.gtm.set_current_led_screen_task(self.gtm.led_screen_tasks.get())

    def clear_queue(self):
        self.to_clear_queue = True

    def kill(self):
        self.is_killed = True

    

class LEDScreenScrollTask(QRunnable):
    def __init__(self, led_screen: QLabel, task_desc: dict) -> None:
        super().__init__()

        self.duration = int(task_desc["duration"])

        self.time_between_updates = 0.5
        self.led_screen = led_screen
        self.text_to_scroll = task_desc["text_to_scroll"]
        self.text_to_display = self.text_to_scroll

        self.current_text_offset = 0

        self.is_killed = False

    @Slot()
    def run(self):
        if self.duration <= 0:
            while True:
                if self.is_killed:
                    return
                try:
                    self.single_loop()
                except RuntimeError:
                    return

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
        led_length = self.led_screen.config.led_screen["width"]
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