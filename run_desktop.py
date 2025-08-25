import webview # type: ignore


# Attendre que le serveur soit prêt (optionnel : ajouter un délai ou un ping)
webview.create_window("Pressing Trois-O", "https://trois-o-services.onrender.com/", width=1200, height=800)
webview.start()