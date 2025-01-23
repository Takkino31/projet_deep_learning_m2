import os
from flask import Flask, request, render_template
from werkzeug.utils import secure_filename
from detection.sift_detection import detect_sift
from detection.cnn_detection import predict_image_authenticity

app = Flask(__name__)

# Dossier où les images uploadées seront stockées
UPLOAD_FOLDER = 'static/uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Crée le dossier d'uploads s'il n'existe pas
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Extensions d'images autorisées
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Fonction pour vérifier si le fichier est une image autorisée
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_image():
    # Vérifie si le fichier est dans la requête
    if 'file' not in request.files:
        return "No file part", 400

    file = request.files['file']
    
    # Si aucun fichier n'a été sélectionné
    if file.filename == '':
        return "No selected file", 400

    # Vérifie que le fichier a la bonne extension
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        # Enregistre le fichier
        file.save(filepath)

        # Vérifie si le fichier est bien enregistré
        if not os.path.exists(filepath):
            return f"Error: file not found at {filepath}", 400

        # Appelle l'analyse SIFT
        sift_similarity, sift_is_falsified = detect_sift(filepath)

        # Appelle la prédiction CNN
        cnn_result = predict_image_authenticity(filepath)

        return render_template(
            'result.html',
            filepath=filepath,
            sift_similarity=sift_similarity,
            sift_is_falsified=sift_is_falsified,
            cnn_result=cnn_result
        )

    return "Invalid file type", 400

if __name__ == '__main__':
    app.run(debug=True)
