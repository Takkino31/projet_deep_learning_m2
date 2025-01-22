import cv2
import numpy as np
import matplotlib.pyplot as plt

def detect_sift(image_path):
    # Charger l'image en niveau de gris
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    # Initialiser l'algorithme SIFT
    sift = cv2.SIFT_create()

    # Détecter les points clés et extraire les descripteurs
    keypoints, descriptors = sift.detectAndCompute(image, None)

    # Diviser l'image en deux moitiés pour la comparaison
    height, width = image.shape
    left_image = image[:, :width//2]
    right_image = image[:, width//2:]

    # Extraire les points clés et les descripteurs pour chaque moitié
    kp1, des1 = sift.detectAndCompute(left_image, None)
    kp2, des2 = sift.detectAndCompute(right_image, None)

    # Utiliser BFMatcher pour comparer les descripteurs des deux moitiés
    bf = cv2.BFMatcher(cv2.NORM_L2, crossCheck=True)
    matches = bf.match(des1, des2)

    # Trier les correspondances par distance
    matches = sorted(matches, key=lambda x: x.distance)

    # Dessiner les correspondances
    image_matches = cv2.drawMatches(left_image, kp1, right_image, kp2, matches[:10], None, flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)

    # Afficher les correspondances
    plt.figure(figsize=(10, 10))
    plt.imshow(image_matches, cmap='gray')
    plt.title('Correspondances entre les deux moitiés de l\'image')
    plt.show()

    # Calculer le pourcentage de correspondances
    num_keypoints = min(len(kp1), len(kp2))
    num_matches = len(matches)
    similarity_percentage = (num_matches / num_keypoints) * 100

    # Déterminer si l'image est falsifiée
    threshold = 15
    is_falsified = similarity_percentage > threshold

    return similarity_percentage, is_falsified
