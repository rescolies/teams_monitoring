import time
import os
import winsound
from pywinauto import Application, Desktop
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class NotificationHandler(FileSystemEventHandler):
    def __init__(self, directory):
        self.directory = directory

    def on_modified(self, event):
        if event.src_path.startswith(self.directory):
            print("Cambio detectado en el directorio de Teams")
            self.check_teams_notifications()

    def on_created(self, event):
        self.on_modified(event)

    def check_teams_notifications(self):
        try:
            app = Application(backend="uia").connect(path="Teams.exe")
            teams_window = app.window(title_re=".*Microsoft Teams")
            teams_window.set_focus()

            # Simula una búsqueda para activar notificaciones
            search_box = teams_window.child_window(auto_id="searchInputField", control_type="Edit")
            search_box.click_input()
            search_box.type_keys("Nuevo mensaje")
            time.sleep(2)  # Espera para que las notificaciones aparezcan

            notifications_pane = teams_window.child_window(title="Activity", control_type="List")
            for item in notifications_pane.descendants():
                if "unread" in item.window_text().lower():
                    print(f"Nueva notificación de Teams detectada: {item.window_text()}")
                    winsound.Beep(1000, 1000)  # Emite un beep de 1 segundo
                    break
        except Exception as e:
            print(f"Error al verificar notificaciones de Teams: {e}")

def monitor_teams_directory(directory):
    event_handler = NotificationHandler(directory)
    observer = Observer()
    observer.schedule(event_handler, path=directory, recursive=False)
    observer.start()
    try:
        while True:
            print("Monitoreando directorio de Teams...")
            time.sleep(10)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

# Directorio que deseas monitorear
teams_directory = "C:\\Users\\TuUsuario\\AppData\\Roaming\\Microsoft\\Teams\\"

# Comienza a monitorear el directorio
monitor_teams_directory(teams_directory)
