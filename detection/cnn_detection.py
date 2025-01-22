import tensorflow as tf
import numpy as np
import os

# Taille de l'image pour DenseNet121
image_size = (224, 224)

# Charger le modèle Keras
model = tf.keras.models.load_model('modele/densenet_model.keras')

def predict_image_authenticity(image_path):
    # Charger l'image et redimensionner
    img = tf.keras.preprocessing.image.load_img(image_path, target_size=image_size)
    img_array = tf.keras.preprocessing.image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = img_array / 255.0

    # Faire la prédiction
    prediction = model.predict(img_array)

    if prediction[0] < 0.5:
        return "authentique"
    else:
        return "falsifiée"
