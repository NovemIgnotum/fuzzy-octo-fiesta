# Pour lancer xvfb-run -a python3 script.py

import os
from playwright.sync_api import sync_playwright

USER_DATA_DIR = "./whatsapp_profile"
GROUP_NAME = "Mon groupe"  # Remplacez par le nom exact de votre groupe
MESSAGE = "Bonjour 👋 Ceci est un message automatique !"

with sync_playwright() as p:
    # Profil persistant pour conserver la session connectée (IndexedDB + cookies)
    context = p.chromium.launch_persistent_context(
        user_data_dir=USER_DATA_DIR,
        headless=False,
        args=[
            "--disable-blink-features=AutomationControlled",
            "--ozone-platform=x11",
        ]
    )

    page = context.pages[0] if context.pages else context.new_page()
    page.goto("https://web.whatsapp.com")

    print("⏳ Chargement de WhatsApp Web...")

    # Attente que l'interface WhatsApp soit chargée (#side est la barre latérale des discussions)
    try:
        page.wait_for_selector('#side', timeout=15000)
        print("✅ Déjà connecté à WhatsApp Web !")
    except Exception:
        print("📲 Veuillez scanner le QR code avec votre téléphone...")
        # Attend jusqu'à 2 minutes que vous scanniez le QR code et que l'interface apparaisse
        page.wait_for_selector('#side', timeout=120000)
        print("✅ Connexion réussie !")

    # Pause courte pour laisser le DOM se stabiliser
    page.wait_for_timeout(3000)

    # 1. Vérifier si le groupe est déjà visible directement dans la liste
    chat_locator = page.locator(f'#side span[title="{GROUP_NAME}"], #side [title="{GROUP_NAME}"]').first
    if chat_locator.is_visible():
        print(f"👉 Groupe '{GROUP_NAME}' trouvé directement dans la liste.")
        chat_locator.click()
    else:
        print(f"🔍 Recherche du groupe : '{GROUP_NAME}'...")
        # Recherche la zone de recherche dans la barre latérale #side
        search_box = page.locator(
            '#side [contenteditable="true"], '
            '#side input, '
            '#side [role="textbox"], '
            '#side [data-testid*="search"]'
        ).first
        search_box.click()
        # Saisie du nom du groupe
        page.keyboard.type(GROUP_NAME, delay=50)
        page.wait_for_timeout(2000)

        # Clic sur le résultat ou touche Entrée
        search_result = page.locator(f'#side span[title="{GROUP_NAME}"], #side [title="{GROUP_NAME}"]').first
        if search_result.is_visible():
            search_result.click()
        else:
            page.keyboard.press("Enter")

    page.wait_for_timeout(2000)

    # 2. Zone de message (dans le footer de la conversation ouverte #main)
    print("✍️ Préparation du message...")
    message_box = page.locator(
        '#main footer [contenteditable="true"], '
        '#main [contenteditable="true"], '
        'footer [contenteditable="true"], '
        'footer [role="textbox"]'
    ).first

    message_box.wait_for(state="visible", timeout=15000)
    message_box.click()
    # Saisie du message
    page.keyboard.type(MESSAGE, delay=30)
    page.wait_for_timeout(500)
    page.keyboard.press("Enter")

    print("🚀 Message envoyé avec succès !")
    page.wait_for_timeout(3000)

    context.close()