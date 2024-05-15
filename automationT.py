import pyautogui
import schedule
import time
import threading
from playsound import playsound

def cambiar_estado():
    # Abre Microsoft Teams (asegúrate de que el atajo esté en la ubicación especificada)
    pyautogui.hotkey('win', 'r')
    pyautogui.typewrite('C:\\Users\\Roger\\AppData\\Local\\Microsoft\\Teams\\Update.exe --processStart "Teams.exe"')
    pyautogui.press('enter')
    time.sleep(10)  # Espera a que Teams se abra
    
    # Cambia el estado a "Conectado" usando la barra de búsqueda
    pyautogui.hotkey('ctrl', 'e')
    time.sleep(2)
    pyautogui.typewrite('/disponible')
    pyautogui.press('enter')

def sonar_alarma():
    while True:
        # Detectar si hay nuevos mensajes en Teams (esto es un ejemplo simple)
        # Necesitas ajustar esto según tu configuración
        if pyautogui.locateOnScreen('mensaje_nuevo.png', confidence=0.8) is not None:
            playsound('alarma.mp3')
            time.sleep(60)  # Espera 60 segundos antes de volver a comprobar
        else:
            time.sleep(5)  # Espera 5 segundos antes de volver a comprobar

def iniciar_alarma():
    alarma_thread = threading.Thread(target=sonar_alarma)
    alarma_thread.daemon = True
    alarma_thread.start()

# Programa principal
def main():
    # Establece la hora en la que quieres cambiar tu estado
    hora_cambio = "20:10"

    # Programa el cambio de estado
    schedule.every().day.at(hora_cambio).do(cambiar_estado)
    
    # Iniciar la alarma en un hilo separado
    iniciar_alarma()

    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    main()