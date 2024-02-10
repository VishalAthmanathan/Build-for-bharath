from flask import Flask, request, jsonify
import os

app = Flask(__name__)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No selected file'})

    # Specify the folder where you want to save the uploaded files
    upload_folder = './Datasets'
    os.makedirs(upload_folder, exist_ok=True)

    file.save(os.path.join(upload_folder, file.filename))

    return jsonify({'success': 'File uploaded successfully'})

if __name__ == '__main__':
    app.run(debug=True)
