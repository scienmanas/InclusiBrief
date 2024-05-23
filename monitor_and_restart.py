# monitor_and_restart.py

import sys
import time
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class RestartHandler(FileSystemEventHandler):
    def __init__(self, script):
        self.script = script
        self.process = None
        self.restart_script()

    def restart_script(self):
        if self.process:
            self.process.terminate()
            self.process.wait()
        self.process = subprocess.Popen([sys.executable, self.script])

    def on_modified(self, event):
        if event.src_path.endswith('.py'):
            print(f"{event.src_path} has been modified. Restarting script.")
            self.restart_script()

    def on_created(self, event):
        if event.src_path.endswith('.py'):
            print(f"{event.src_path} has been created. Restarting script.")
            self.restart_script()

    def on_deleted(self, event):
        if event.src_path.endswith('.py'):
            print(f"{event.src_path} has been deleted. Restarting script.")
            self.restart_script()

if __name__ == "__main__":
    path = "."  # Watch the current directory
    script_to_watch = "multipurpose_bot.py"
    
    event_handler = RestartHandler(script_to_watch)
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
