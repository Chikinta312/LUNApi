![Demo de LUNA](images/Logo%20LUNA3.0.png)

# LUNA 3.0 – Asistente Virtual por Voz

**LUNA 3.0** es un asistente virtual activado por comandos de voz, diseñado para brindar soporte y compañía a personas con movilidad reducida en el hogar. Desarrollado en Python y optimizado para funcionar en sistemas operativos como Windows o una Raspberry Pi 5, LUNA integra reconocimiento de voz, síntesis de voz natural, consultas inteligentes, lectura de noticias vía RSS, clima, calendario, y más.

---

## 📌 Introducción

El objetivo de **LUNA 3.0** es ofrecer un sistema de asistencia inteligente que permita interactuar por voz con tareas cotidianas o de oficina.

Este proyecto forma parte de una tesis universitaria y emplea tecnologías de código abierto como `SpeechRecognition`, `pyttsx3`, `feedparser`, `requests`, y `Ollama` (para acceder al modelo de lenguaje Gemma3 1B).

---

## ⚙️ Requisitos Mínimos

* **Raspberry Pi 5 (4 GB RAM mínimo)** - Recomendado **8 GB RAM**
* **Sistema operativo Raspberry Pi OS Lite (64 bits)** - Recomendado **Raspberry Pi OS (64 bits)**
* **Python 3.13.3 o superior**
* **Conexión a internet**
* **Micrófono USB o incorporado**
* **Parlante o salida de audio funcional** (Funciona también con parlantes Bluetooth)
* **Tarjeta SD de 16 GB o superior** (Si desea usar otros modelos se recomienda aumentar a mínimo 64 GB)

### Librerías necesarias:

```bash
pip install SpeechRecognition
pip install pyttsx3
pip install feedparser
pip install requests
pip install pyaudio
pip install sounddevice
pip install gTTS
pip install playsound
```

---

Para instalar tu asistente virtual **LUNA 3.0** en una Raspberry Pi 5 (u otro sistema compatible), sigue los siguientes pasos:

---

## 🛠️ Instalación

Sigue los siguientes pasos para instalar y ejecutar **LUNA 3.0** en tu dispositivo:

### 1. **Clona el repositorio**

```bash
git clone https://github.com/Chikinta312/LUNApi.git
cd LUNApi
```

### 2. **Crea y activa un entorno virtual (opcional pero recomendado)**

```bash
python3 -m venv env
source env/bin/activate  # En Linux o macOS
env\Scripts\activate     # En Windows
```

### 3. **Instala las dependencias**

```bash
pip install -r requirements.txt
```

> Asegúrate de que `requirements.txt` esté correctamente definido. Si no lo tienes, puedes usar el siguiente comando para generar uno:

```bash
pip freeze > requirements.txt
```

### 4. **Configura tu micrófono y parlante**

* Verifica que el micrófono USB y el parlante funcionen correctamente.
* Puedes probar con comandos como `arecord` y `aplay` en Raspberry Pi OS.

### 5. **Instala Ollama y el modelo Gemma3:1b**

Para instalar **Ollama** en tu Raspberry Pi, ejecuta el siguiente comando:

```bash
curl -fsSL https://ollama.com/install.sh | sh
```

Para ejecutar el modelo **Gemma3:1b**, usa el siguiente comando:

```bash
ollama run gemma3:1b
```

> **Nota**: Si deseas ejecutar el modelo Gemma3:1b como servicio para que se inicie automáticamente al arrancar la Raspberry Pi, puedes agregarlo a los servicios de inicio.

### 6. **Ejecuta el asistente**

Ojo: debes estar dentro del entorno virtual:

```bash
python luna_asistente.py
```

---

### 📌 **Notas adicionales**

* Asegúrate de estar conectado a internet.
* Este proyecto utiliza el modelo **Gemma3 1B**, que es compatible con una Raspberry Pi 5 con 4GB de RAM. Si deseas usar modelos más grandes (como 4B, 12B), necesitarás una Raspberry Pi con más RAM (8GB o 16GB).
* El modelo **Gemma3 1B** debe estar corriendo en Ollama. Puedes iniciarlo con el siguiente comando:

```bash
ollama run gemma3:1b
```

* Si deseas configurar el modelo como servicio o usar comandos de voz para activarlo, añade detalles en `config.py` o donde se defina la lógica.

---

## 🧠 Funcionalidades

* 📣 **Activación por voz** mediante comando personalizado.
* 🗣️ **Síntesis de voz natural** (TTS).
* 🔍 **Consultas inteligentes** usando Gemma3 1B vía Ollama.
* 🌦️ **Informe del clima** en tiempo real.
* 📰 **Lectura de noticias** usando fuentes RSS.
* 📅 **Gestión de fechas** (día, hora, recordatorios simples).
* 🛠️ **Diseño modular**, preparado para ampliaciones futuras (OpenHAB, sensores IoT, etc.).

---

## 🔒 **Privacidad de los datos**

LUNA 3.0 procesa los datos de forma local en la Raspberry Pi, lo que garantiza un mayor control sobre la privacidad del usuario. No se envía información personal a servidores externos sin consentimiento.

---

## 👨‍💻 **Autor**

**Fabián Andrés Chiquinta Veramendi**
Estudiante de Ingeniería Electrónica – UTP

📧 Contacto: [fabian312chv@gmail.com](mailto:fabian312chv@gmail.com)

🔗 GitHub: [https://github.com/Chikinta312](https://github.com/Chikinta312)

---

## 📄 **Licencia**

Este proyecto está bajo la Licencia MIT. Consulta el archivo [LICENSE](LICENSE) para más información.

---

## 🤝 **Agradecimientos**

* OpenAI y Google por sus herramientas de NLP.
* Comunidad de Raspberry Pi y Python.
* Docentes asesores y colaboradores del proyecto.

---

> “La voz es el puente entre la tecnología y la humanidad.”

---

Este README está ahora actualizado con la información completa y clara, incluyendo la instalación de Ollama y el modelo Gemma3:1b, con instrucciones precisas para la Raspberry Pi. ¡Espero que sea útil!
