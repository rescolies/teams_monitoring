import asyncio
from playsound import playsound
from winrt.windows.ui.notifications.management import UserNotificationListener, UserNotificationListenerAccessStatus

async def get_teams_notifications():
    listener = UserNotificationListener.get_current()
    access_status = await listener.request_access_async()

    if access_status != UserNotificationListenerAccessStatus.ALLOWED:
        print("Acceso denegado a las notificaciones del sistema")
        return False

    # Llamar a get_notifications_async y manejar la tarea correctamente
    notifications = await listener.get_notifications_async().as_future()

    for notification in notifications:
        app_info = notification.app_info
        if "Teams" in app_info.display_name:
            return True

    return False

async def sonar_alarma():
    while True:
        try:
            if await get_teams_notifications():
                playsound('alarma.mp3')
                await asyncio.sleep(60)  # Espera 60 segundos antes de volver a comprobar
        except Exception as e:
            print(f"Error al obtener notificaciones: {e}")
        await asyncio.sleep(1)  # Evita bloquear el bucle de eventos

# Programa principal
async def main():
    await sonar_alarma()

# Ejecuta el programa principal
if __name__ == "__main__":
    asyncio.run(main())
