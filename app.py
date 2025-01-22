from flask import Flask, render_template, request, url_for
import os
from detection.sift_detection import detect_sift
from detection.cnn_detection import predict_image_authenticity

app = Flask(__name__)

# Répertoire où les images téléchargées seront stockées
UPLOAD_FOLDER = 'static/upload'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Assurez-vous que le dossier existe
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        return 'Aucun fichier sélectionné.'

    file = request.files['file']
    if file.filename == '':
        return 'Aucun fichier sélectionné.'

    # Sauvegarder l'image dans le répertoire des uploads
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(filepath)

    # Analyser l'image avec SIFT
    sift_similarity, sift_is_falsified = detect_sift(filepath)

    # Analyser l'image avec DenseNet
    densenet_result = predict_image_authenticity(filepath)

    # Rendre la page de résultat avec les résultats des deux méthodes
    return render_template('result.html', 
                           sift_similarity=sift_similarity, 
                           sift_is_falsified=sift_is_falsified, 
                           densenet_result=densenet_result, 
                           filepath=filepath)

if __name__ == '__main__':
    app.run(debug=True)
