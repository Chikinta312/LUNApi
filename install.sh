#!/bin/bash
echo "🚀 Instalando dependencias para el asistente LUNA..."

sudo apt update
sudo apt install -y python3 python3-pip python3-dev espeak ffmpeg portaudio19-dev unzip git libffi-dev

echo "📦 Instalando bibliotecas de Python..."
pip3 install vosk pyttsx3 sounddevice llama-cpp-python

echo "⬇️ Descargando modelo Vosk (español pequeño)..."
mkdir -p modelos/vosk
wget -O vosk-es.zip https://alphacephei.com/vosk/models/vosk-model-small-es-0.42.zip
unzip vosk-es.zip -d modelos/vosk_temp
mv modelos/vosk_temp/* modelos/vosk
rm -rf modelos/vosk_temp vosk-es.zip

echo "⬇️ Descargando modelo TinyLLaMA GGUF..."
wget -O modelos/TinyLlama-1.1B-Chat-v1.0.Q4_K_M.gguf https://huggingface.co/TheBloke/TinyLlama-1.1B-Chat-v1.0-GGUF/resolve/main/TinyLlama-1.1B-Chat-v1.0.Q4_K_M.gguf

echo "✅ Instalación completa. Puedes ejecutar el asistente con: python3 asistente.py"