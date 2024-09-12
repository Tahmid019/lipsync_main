from flask import Flask, request, jsonify
import os
from moviepy.editor import VideoFileClip
import speech_recognition as sr

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads/'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'video' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400

    file = request.files['video']
    
    if file.filename == '':
        return jsonify({'error': 'No file selected for uploading'}), 400

    if file:
        filename = file.filename
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        try:
            video = VideoFileClip(file_path)
            audio_path = os.path.join(app.config['UPLOAD_FOLDER'], 'extracted_audio.wav')
            video.audio.write_audiofile(audio_path)

            recognizer = sr.Recognizer()
            with sr.AudioFile(audio_path) as source:
                audio = recognizer.record(source)

            text = recognizer.recognize_google(audio)
            return jsonify({'message': 'File successfully uploaded', 'transcription': text}), 200
        
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    return jsonify({'error': 'File not allowed'}), 400

if __name__ == '__main__':
    app.run(debug=True, port=5000)