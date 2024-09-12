import express from 'express';
import fileUpload from 'express-fileupload';
import path from 'path';
import { fileURLToPath } from 'url';
import fs from 'fs';
import { exec } from 'child_process';
import util from 'util';
import speech from '@google-cloud/speech';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const app = express();
const UPLOAD_FOLDER = path.join(__dirname, 'uploads');
const execPromise = util.promisify(exec);

// Create uploads folder if it doesn't exist
if (!fs.existsSync(UPLOAD_FOLDER)) {
    fs.mkdirSync(UPLOAD_FOLDER);
}

app.use(fileUpload());
app.use(express.static(path.join(__dirname, 'build'))); // Assuming 'build' folder contains your React app

app.post('/upload', async (req, res) => {
    if (!req.files || !req.files.video) {
        return res.status(400).json({ error: 'No file part in the request' });
    }

    const file = req.files.video;

    if (!file.name) {
        return res.status(400).json({ error: 'No file selected for uploading' });
    }

    const filePath = path.join(UPLOAD_FOLDER, file.name);
    await file.mv(filePath);

    try {
        const audioPath = path.join(UPLOAD_FOLDER, 'extracted_audio.wav');

        // Extract audio using ffmpeg
        await execPromise(`ffmpeg -i "${filePath}" -q:a 0 -map a "${audioPath}"`);

        // Transcribe audio using Google Cloud Speech-to-Text
        const client = new speech.SpeechClient();
        const audioBytes = fs.readFileSync(audioPath).toString('base64');

        const audio = {
            content: audioBytes,
        };
        const config = {
            encoding: 'LINEAR16',
            sampleRateHertz: 16000,
            languageCode: 'en-US',
        };
        const request = {
            audio: audio,
            config: config,
        };

        const [response] = await client.recognize(request);
        const transcription = response.results
            .map(result => result.alternatives[0].transcript)
            .join('\n');

        return res.status(200).json({ message: 'File successfully uploaded', transcription: transcription });

    } catch (error) {
        return res.status(500).json({ error: error.message });
    }
});

app.get('*', (req, res) => {
    res.sendFile(path.join(__dirname, 'build', 'index.html'));
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
    console.log(`Server is running on port ${PORT}`);
});
