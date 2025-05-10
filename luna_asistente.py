import os
import requests
import json
import re
import tempfile
import sounddevice as sd
import numpy as np
import speech_recognition as sr
import locale
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
import feedparser
from gtts import gTTS
from playsound import playsound

# Establecer conexion con Home assistant:
HOME_ASSISTANT_URL = "http://localhost:8123"  # O la IP si no es en la misma máquina

def obtener_token():
    try:
        with open("token.txt", "r") as f:
            return f.read().strip()
    except FileNotFoundError:
        speak("❌ No se encontró el archivo de token.")
        return None

# Establecer la configuración regional para que las fechas se muestren en español
locale.setlocale(locale.LC_TIME, "es_ES.UTF-8")

def speak(text):
    """Función para que el asistente hable directamente desde la memoria usando gTTS."""
    print(f"Luna: {text}")
    try:
        tts = gTTS(text=text, lang='es', slow=False)
        with tempfile.NamedTemporaryFile(delete=True, suffix=".mp3") as fp:
            tts.save(fp.name)
            playsound(fp.name)
    except Exception as e:
        print(f"❌ Error al reproducir la voz: {e}")

def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎙️ Di algo...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    try:
        return recognizer.recognize_google(audio, language="es-ES")
    except sr.UnknownValueError:
        return ""
    except sr.RequestError:
        speak("❌ Error de conexión con el servicio de reconocimiento.")
        return ""

def detectar_pregunta_local(texto):
    texto = texto.lower()
    if "clima" in texto:
        return "clima"
    elif "evento" in texto or "calendario" in texto:
        return "eventos"
    elif "noticias" in texto:
        return "noticias"
    elif "hora" in texto:
        return "hora"
    elif "fecha" in texto or "día" in texto or "semana" in texto:
        return "fecha"
    elif "mañana" in texto or "pasado mañana" in texto:
        return "futuro"
    elif any(d in texto for d in ["lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"]):
        return "dias_semana"
    elif "falta" in texto or "cuánto falta" in texto:
        return "falta_fecha"
    return None

def responder_pregunta_local(tipo):
    ahora = datetime.now()
    if tipo == "hora":
        return f"Son las {ahora.strftime('%H:%M')}."
    elif tipo == "fecha":
        return f"Según 📅 Hoy es {ahora.strftime('%A, %d de %B de %Y')}."

def responder_fecha_futura(momento):
    ahora = datetime.now()
    days = 1 if momento == "mañana" else 2
    fecha = ahora + timedelta(days=days)
    return f"De acuerdo al 📅 {momento.capitalize()} será {fecha.strftime('%A, %d de %B de %Y')}."

def responder_dias_semana(dia):
    hoy = datetime.now()
    dias = {"lunes": 0, "martes": 1, "miercoles": 2, "jueves": 3, "viernes": 4, "sabado": 5, "domingo": 6}
    dia_objetivo = dias.get(dia.lower())
    if dia_objetivo is None:
        return "❌ No entendí qué día mencionaste."
    diferencia = (dia_objetivo - hoy.weekday()) % 7
    fecha = hoy + timedelta(days=diferencia)
    return f"En el 📅 dice que el próximo {dia} será {fecha.strftime('%A, %d de %B de %Y')}."

def dias_faltantes_para_fecha(texto):
    match = re.search(r'(\d{1,2})\s+de\s+(enero|febrero|marzo|abril|mayo|junio|julio|agosto|septiembre|octubre|noviembre|diciembre)', texto.lower())
    if not match:
        return "❌ No pude entender la fecha que mencionaste."
    dia = int(match.group(1))
    mes = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"].index(match.group(2)) + 1
    hoy = datetime.now()
    fecha_obj = datetime(hoy.year, mes, dia)
    if hoy > fecha_obj:
        fecha_obj = datetime(hoy.year + 1, mes, dia)
    dias = (fecha_obj - hoy).days
    return f"📅 Faltan {dias} días para el {fecha_obj.strftime('%d de %B de %Y')}."

def obtener_noticias():
    url = "https://news.google.com/rss?hl=es-419&gl=PE&ceid=PE:es"
    noticias = feedparser.parse(url)
    if not noticias.entries:
        return "❌ No se encontraron noticias."

    resultado = ""
    fuentes_usadas = set()
    contador = 0
    for entrada in noticias.entries:
        fuente = entrada.get("source", {}).get("title", "Fuente desconocida")
        if fuente in fuentes_usadas:
            continue
        titular = BeautifulSoup(entrada.title, "html.parser").get_text().strip()
        if contador == 0:
            resultado += f"{titular} (Fuente: {fuente})"
        else:
            resultado += f"\n{titular} (Fuente: {fuente})"
        fuentes_usadas.add(fuente)
        contador += 1
        if contador == 5:
            break

    if contador == 0:
        return "❌ No se encontraron noticias únicas de diferentes fuentes."

    return resultado.strip()

def consultar_clima(ciudad="Lima"):
    try:
        response = requests.get(f"https://wttr.in/{ciudad}?format=3", timeout=5)
        if response.ok:
            return response.text
        else:
            return "❌ No se pudo obtener el clima en este momento."
    except Exception:
        return "❌ No se pudo acceder al servicio del clima."

def ask_ollama_streaming(prompt):
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": "gemma3:1b", "prompt": f"Responde en español de forma clara y natural. {prompt}", "stream": True},
            stream=True,
            timeout=60
        )
        if response.ok:
            buffer = ""
            for line in response.iter_lines():
                if line:
                    data = json.loads(line.decode("utf-8"))
                    chunk = data.get("response", "").replace("*", "")
                    print(chunk, end="", flush=True)
                    buffer += chunk
                    if len(buffer) >= 20 and chunk.endswith((".", ",", " ")):
                        speak(buffer.strip())
                        buffer = ""
            if buffer:
                speak(buffer.strip())
        else:
            speak("❌Hubo un error al contactar con el modelo.")
    except requests.exceptions.Timeout:
        speak("❌La solicitud tardó demasiado en responder.")
    except Exception as e:
        speak(f"❌Error de conexión: {e}")

def main():
    print("Iniciando asistente...")
    speak("Hola, soy Luna, tu asistente personal. Di 'Luna' seguido de tu solicitud para comenzar.")
    while True:
        print("Esperando comandos...")
        user_input = listen()
        if not user_input:
            continue
        print(f"Comando recibido: {user_input}")
        tipo_pregunta = detectar_pregunta_local(user_input)
        
        if tipo_pregunta == "clima":
            respuesta = consultar_clima()
            speak(respuesta)
        elif tipo_pregunta == "eventos":
            respuesta = "Lo siento, no tengo información sobre eventos por ahora."
            speak(respuesta)
        elif tipo_pregunta == "noticias":
            respuesta = obtener_noticias()
            speak(respuesta)
        elif tipo_pregunta == "hora":
            respuesta = responder_pregunta_local("hora")
            speak(respuesta)
        elif tipo_pregunta == "fecha":
            respuesta = responder_pregunta_local("fecha")
            speak(respuesta)
        elif tipo_pregunta == "futuro":
            respuesta = responder_fecha_futura(user_input)
            speak(respuesta)
        elif tipo_pregunta == "dias_semana":
            dia = re.search(r"lunes|martes|miércoles|jueves|viernes|sábado|domingo", user_input.lower()).group(0)
            respuesta = responder_dias_semana(dia)
            speak(respuesta)
        elif tipo_pregunta == "falta_fecha":
            respuesta = dias_faltantes_para_fecha(user_input)
            speak(respuesta)
        else:
            # Si no es un comando predefinido, preguntamos a Ollama
            speak("Lo siento, no entendí la pregunta. Consultando a Ollama...")
            ask_ollama_streaming(user_input)

if __name__ == "__main__":
    main()
