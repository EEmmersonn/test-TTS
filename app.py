# app.py

import wave
from piper import PiperVoice, SynthesisConfig

# === 1. Загрузка голоса ===
# Укажи точное имя модели (должно совпадать с именем после download_voices)
model_name = "en_US-lessac-medium"  # или путь к .onnx файлу: "voices/en_US-lessac-medium.onnx"

# 🔥 Раскомментируй, если хочешь использовать GPU
# voice = PiperVoice.load(f"{model_name}.onnx", use_cuda=True)

# Для CPU (рекомендуется, если нет GPU):
voice = PiperVoice.load(f"{model_name}.onnx")

print(f"Голос '{model_name}' загружен.")

# === 2. Настройки синтеза ===
syn_config = SynthesisConfig(
    volume=1.0,           # громкость: 1.0 = норма
    length_scale=1.0,     # 1.0 = норма, >1 = медленнее
    noise_scale=0.75,     # 🔥 вариативность интонации (рекомендуется 0.6–0.8)
    noise_w_scale=0.8,    # вариативность длительности звуков
    normalize_audio=True  # нормализовать аудио (рекомендуется)
)

# === 3. Текст для озвучки ===
text = "Welcome to the world of speech synthesis with Piper!"

# === 4. Синтез в .wav файл ===
output_path = "output/test.wav"

with wave.open(output_path, "w") as wav_file:
    voice.synthesize_wav(text, wav_file, syn_config=syn_config)

print(f"Аудио сохранено: {output_path}")