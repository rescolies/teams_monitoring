import os
import time
import winsound
import subprocess
import requests
from pywinauto import Desktop, Application

def iniciar_teams():
    # Abre Microsoft Teams usando subprocess
    subprocess.Popen(['C:\\Users\\Roger\\AppData\\Local\\Microsoft\\Teams\\Update.exe', '--processStart', 'Teams.exe'])
    time.sleep(15)  # Espera a que Teams se abra

def sonar_alarma():
    duration = 500  # Duración en milisegundos
    freqs = [440, 880, 660, 990]  # Frecuencias en Hz
    for i in range(10):  # Cambiar el sonido 10 veces
        for freq in freqs:
            winsound.Beep(freq, duration)

def enviar_notificacion_movil(mensaje):
    # Configura tu User Key y API Token de Pushover
    user_key = 'TU_USER_KEY'
    api_token = 'TU_API_TOKEN'
    
    # Enviar la notificación a través de la API de Pushover
    url = "https://api.pushover.net/1/messages.json"
    payload = {
        "token": api_token,
        "user": user_key,
        "message": mensaje,
        "title": "Notificación de Microsoft Teams"
    }
    response = requests.post(url, data=payload)
    if response.status_code == 200:
        print("Notificación enviada al móvil.")
    else:
        print(f"Error al enviar notificación: {response.status_code} - {response.text}")

def verificar_notificaciones():
    try:
        # Usar Desktop para buscar la ventana de notificación
        print("Buscando notificaciones de Microsoft Teams...")
        desktop = Desktop(backend="uia")

        # Buscar la ventana de notificación de Microsoft Teams
        notification_window = None
        for window in desktop.windows():
            if "Notificación de Microsoft Teams" in window.window_text():
                notification_window = window
                break

        if notification_window:
            print("Notificación de Microsoft Teams detectada.")
            sonar_alarma()
            enviar_notificacion_movil("Se ha detectado una notificación de Microsoft Teams.")
            return True
        else:
            print("No se detectaron nuevas notificaciones.")
            return False
    except Exception as e:
        print(f"Error al verificar notificaciones de Teams: {e}")
        return False

def main():
    iniciar_teams()
    while True:
        if verificar_notificaciones():
            print("Alarma sonando. No se harán comprobaciones adicionales durante este tiempo.")
            sonar_alarma()  # Suena la alarma sin hacer comprobaciones adicionales
        time.sleep(10)  # Verifica cada 10 segundos

if __name__ == "__main__":
    main()
