import webview # type: ignore
import os
import threading

def start_django():
    os.system("python manage.py runserver")


# Lancer Django dans un thread séparé
threading.Thread(target=start_django, daemon=True).start()

# Attendre que le serveur soit prêt (optionnel : ajouter un délai ou un ping)
webview.create_window("Pressing Trois-O", "http://127.0.0.1:8000/login", width=1200, height=800)
webview.start()