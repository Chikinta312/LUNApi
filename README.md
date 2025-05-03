# Asistente de Voz LUNA

Asistente de voz activado por la palabra clave "Luna", usando Vosk para reconocimiento de voz y TinyLLaMA para respuestas. Funciona en Raspberry Pi OS Lite 64 bits.

## 🔧 Instalación

```bash
git clone https://github.com/TU_USUARIO/asistente_luna.git
cd asistente_luna
chmod +x install.sh
./install.sh
```

## ▶️ Uso

```bash
python3 asistente.py
```

## 🚀 Iniciar automáticamente al encender

```bash
sudo cp asistente.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable asistente.service
sudo systemctl start asistente.service
```

## ✅ Requisitos

- Raspberry Pi OS Lite 64 bits
- Micrófono USB
- Tarjeta SD de al menos 16 GB