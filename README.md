![Demo de LUNA](images/Logo%20LUNA3.0.png)


# LUNA 3.0 – Asistente Virtual por Voz

**LUNA 3.0** es un asistente virtual activado por comandos de voz, diseñado para brindar soporte
y compañía a personas con movilidad reducida en el hogar. Desarrollado en Python y optimizado
para funcionar en una Raspberry Pi 5, LUNA integra reconocimiento de voz, síntesis de voz natural,
consultas inteligentes, lectura de noticias vía RSS, clima, calendario, y más.

---

## 📌 Introducción

El objetivo de LUNA 3.0 es ofrecer un sistema de asistencia inteligente que permita interactuar
por voz con tareas cotidianas o de oficina.

Este proyecto forma parte de una tesis universitaria y emplea tecnologías de código abierto
como `SpeechRecognition`, `pyttsx3`, `feedparser`, `requests`, y `Ollama`
(para acceder al modelo de lenguaje Gemma3 1B).

---

## ⚙️ Requisitos Minimos:

- Raspberry Pi 5 (4 GB RAM recomendado)
- Sistema operativo Raspberry Pi OS (64 bits)
- Python 3.13.3 o superior
- Conexión a internet
- Micrófono USB o incorporado
- Parlante o salida de audio funcional
- Tarjeta SD de 16 GB o superior

### Librerías necesarias:

```bash
pip install SpeechRecognition
pip install pyttsx3
pip install feedparser
pip install requests
pip install pyaudio
````

---

Para instalar tu asistente virtual **LUNA 3.0** en una Raspberry Pi 5 (u otro sistema compatible), debes seguir los siguientes pasos.

---

## 🛠️ Instalación

Sigue los siguientes pasos para instalar y ejecutar LUNA 3.0 en tu dispositivo:

Para Windows solo descargar el archivo Python y subirlo a tu Visual Studio Code, se recomienda instalar previamente Ollama en tu dispositivo
con la version de su modelo que desee utilziar (el codigo esta diseñado para el modelo Gemma3:1b)

### 1. Clona el repositorio

```bash
git clone https://github.com/Chikinta312/LUNApi.git
cd LUNApi
```

### 2. Crea y activa un entorno virtual (opcional pero recomendado)

```bash
python3 -m venv env
source env/bin/activate  # En Linux o macOS
env\Scripts\activate     # En Windows
```

### 3. Instala las dependencias

```bash
pip install -r requirements.txt
```

> Asegúrate de que `requirements.txt` esté correctamente definido. Si no lo tienes, puedo ayudarte a generarlo.

### 4. Configura tu micrófono y parlante

* Verifica que el micrófono USB y el parlante funcionen correctamente.
* Puedes probar con comandos como `arecord` y `aplay` en Raspberry Pi OS.

### 5. Ejecuta el asistente

Ojo: debes estar dentro del entorno virtual:
```bash
python luna_asistente.py
```

---

### 📌 Notas adicionales

* Asegúrate de estar conectado a internet.
* En este caso se uso el modelo Gemma3 1B, debido que es el unico modelo que puede arrancar en una RPI5B de 4GB RAM. 
  Si desea usar los Modelos (4b, 12b) tendra que usar una RPI de 8GB RAM en adelante, para el 27b usar una RPI de 16GB RAM.
* El modelo Gemma3 1B debe estar corriendo en Ollama. Puedes iniciarlo con:

```bash
ollama run gemma:1b
```

* Si deseas configurar el modelo como servicio o usar comandos de voz para activarlo, añade detalles en `config.py` o donde se defina la lógica.

---

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

## 🔒 Privacidad de los datos

LUNA 3.0 procesa los datos de forma local en la Raspberry Pi, lo que garantiza un mayor control sobre 
la privacidad del usuario. No se envía información personal a servidores externos sin consentimiento.

---

## 👨‍💻 Autor

**Fabián Andrés Chiquinta Veramendi**
Estudiante de Ingeniería Electrónica – UTP

📧 Contacto: \[[fabian312chv@gmail.com](mailto:fabian312chv@gmail.com)]

🔗 GitHub: [https://github.com/Chikinta312](https://github.com/Chikinta312)

---

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Consulta el archivo [LICENSE](LICENSE) para más información.

---

## 🤝 Agradecimientos

* OpenAI y Google por sus herramientas de NLP.
* Comunidad de Raspberry Pi y Python.
* Docentes asesores y colaboradores del proyecto.

---

> “La voz es el puente entre la tecnología y la humanidad.”

```

¿Te gustaría que también te genere el archivo `requirements.txt` para este proyecto?
```
