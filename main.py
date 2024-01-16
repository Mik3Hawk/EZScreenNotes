# Importation des modules nécessaires
import time
import pyautogui
import os
from PIL import Image
from selenium import webdriver
from reportlab.pdfgen import canvas

def prendre_captures(url, nom_fichier, nombre_max_captures):
    # Initialisation du navigateur Chrome
    navigateur = webdriver.Chrome(options=webdriver.ChromeOptions())

    captures = []  # Liste pour stocker les noms des fichiers des captures

    try:
        # Accès à l'URL spécifiée
        navigateur.get(url)
        navigateur.implicitly_wait(5)

        # Compteur pour garder l'ordre d'origine des captures
        compteur = 1

        # Boucle pour prendre des captures d'écran jusqu'à atteindre le nombre maximum ou détecter une capture identique
        for i in range(1, nombre_max_captures + 1):
            capture_nom = nom_fichier.format(compteur)
            navigateur.save_screenshot(capture_nom)
            captures.append(capture_nom)

            # Vérification si la capture actuelle est identique à la précédente
            if i > 1 and os.path.exists(captures[-1]) and os.path.exists(captures[-2]):
                if open(captures[-1], "rb").read() == open(captures[-2], "rb").read():
                    print(f"Les captures {captures[-1]} et {captures[-2]} sont identiques. Arrêt de la boucle.")
                    break

            # Simuler un clic en bas à droite de l'écran avec pyautogui
            largeur_ecran, hauteur_ecran = pyautogui.size()
            pyautogui.click(largeur_ecran - 650, hauteur_ecran - 140)  # À MODIFIER
            # Modifiez les dimensions x, y jusqu'à ce que votre curseur soit sur la flèche droite en bas de l'écran

            # Pause entre chaque capture d'écran
            time.sleep(0.5)

            # Incrémenter le compteur
            compteur += 1

    except Exception as e:
        print(f"Une erreur s'est produite : {e}")

    finally:
        # Fermeture du navigateur
        navigateur.quit()

    # Retourner la liste des captures
    return captures

def creer_pdf(captures, output_pdf):
    # Initialisation du canvas PDF avec les dimensions de l'écran
    pdf = canvas.Canvas(output_pdf, pagesize=(pyautogui.size()[0], pyautogui.size()[1]))

    # Ajouter les images au PDF seulement si elles existent
    for capture in captures:
        if os.path.exists(capture):
            # Ajout d'une nouvelle page
            pdf.showPage()

            # Ajout de l'image au canvas PDF
            draw_image(pdf, capture, 0, 0, pyautogui.size()[0], pyautogui.size()[1])

    # Enregistrement du PDF final
    pdf.save()

def supprimer_captures(captures):
    for capture in captures:
        try:
            os.remove(capture)
            print(f"Fichier supprimé : {capture}")
        except Exception as e:
            print(f"Une erreur s'est produite lors de la suppression de {capture} : {e}")

def draw_image(pdf, image_path, x, y, width, height):
    # Vérifier si le fichier existe avant d'ajouter l'image au PDF
    if os.path.exists(image_path):
        # Ouverture de l'image pour obtenir ses dimensions
        image = Image.open(image_path)
        # Ajout de l'image au canvas PDF avec les dimensions correctes
        pdf.drawImage(image_path, x, y, width=width, height=height, preserveAspectRatio=True)

def main():
    url_du_site = "https://dullin.github.io/TCH056/diapos/ch4_javascript/"  # À MODIFIER, entrez l'url du site désiré
    nom_du_fichier = "capture_page_{}.png"
    nombre_max_captures = 200  # 100 par défaut, peut être augmenté
    output_pdf = 'output3.pdf'  # output.pdf par défaut, peut être modifié

    # Étape 1 : Prendre les captures d'écran
    captures = prendre_captures(url_du_site, nom_du_fichier, nombre_max_captures)

    # Laisser du temps à l'utilisateur pour effectuer le tri manuel
    input("Appuyez sur Entrée après avoir supprimé les captures inutiles dans le dossier.")

    # Étape 2 : Créer le PDF avec les captures restantes
    creer_pdf(captures, output_pdf)

    # Étape 3 : Supprimer les captures d'écran du dossier
    supprimer_captures(captures)

if __name__ == "__main__":
    main()
