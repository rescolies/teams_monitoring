import time
import winsound
from pywinauto import Application
from pywinauto import Desktop

def iniciar_teams():
    # Abre Microsoft Teams (asegúrate de que el atajo esté en la ubicación especificada)
    os.system('start "" "C:\\Users\\TuUsuario\\AppData\\Local\\Microsoft\\Teams\\Update.exe --processStart Teams.exe"')
    time.sleep(10)  # Espera a que Teams se abra

def sonar_alarma():
    duration = 1000  # Duración en milisegundos
    freq = 440  # Frecuencia en Hz
    winsound.Beep(freq, duration)

def verificar_notificaciones():
    try:
        app = Application(backend="uia").connect(path="Teams.exe")
        teams_window = app.window(title_re=".*Microsoft Teams")
        teams_window.set_focus()

        # Verifica si hay notificaciones de mensajes nuevos
        notifications = teams_window.child_window(title="Activity", control_type="Pane")
        
        if notifications.exists():
            for item in notifications.children():
                if "unread" in item.window_text().lower():
                    print(f"Nueva notificación de Teams detectada: {item.window_text()}")
                    sonar_alarma()
                    return True
        return False
    except Exception as e:
        print(f"Error al verificar notificaciones de Teams: {e}")
        return False

def main():
    iniciar_teams()
    while True:
        if not verificar_notificaciones():
            print("No se detectaron nuevas notificaciones.")
        time.sleep(10)  # Verifica cada 10 segundos

if __name__ == "__main__":
    main()
