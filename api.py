# api.py - простой API для Piper TTS

from flask import Flask, request, send_file, jsonify
from piper import PiperVoice, SynthesisConfig
import wave
import os
import tempfile

app = Flask(__name__)

# 🎙️ Загружаем голос при старте
MODEL_PATH = "voices\en_US-lessac-medium.onnx"  # или en_US-lessac-medium
if not os.path.exists(MODEL_PATH):
    print(f"Модель не найдена: {MODEL_PATH}")
    print("Положи модель в папку voices/")
    exit(1)

print("Загружаем модель...")
voice = PiperVoice.load(MODEL_PATH)
print("Готово.")

# Настройки по умолчанию
DEFAULT_CONFIG = SynthesisConfig(
    volume=1.0,
    length_scale=1.1,
    noise_scale=0.75,
    noise_w_scale=0.8,
    normalize_audio=True
)

@app.route('/tts', methods=['POST'])
def tts():
    data = request.get_json()
    text = data.get('text', '').strip()

    if not text:
        return jsonify({"error": "Поле 'text' обязательно"}), 400

    # Поддержка параметров (опционально)
    length_scale = float(data.get('length_scale', 1.1))
    noise_scale = float(data.get('noise_scale', 0.75))
    noise_w_scale = float(data.get('noise_w_scale', 0.8))

    custom_config = SynthesisConfig(
        volume=1.0,
        length_scale=length_scale,
        noise_scale=noise_scale,
        noise_w_scale=noise_w_scale,
        normalize_audio=True
    )

    # Создаём временный .wav файл
    temp_wav = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
    temp_wav.close()

    try:
        with wave.open(temp_wav.name, "w") as wav_file:
            voice.synthesize_wav(text, wav_file, syn_config=custom_config)

        # Отправляем файл
        return send_file(temp_wav.name, as_attachment=True, download_name="speech.wav", mimetype="audio/wav")

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "ok", "model": MODEL_PATH}), 200

if __name__ == '__main__':
    print("Запуск API на http://localhost:5000")
    app.run(host='0.0.0.0', port=5000)