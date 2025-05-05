import os
import requests
import json
import re
import pyttsx3
import sounddevice as sd
import numpy as np
import speech_recognition as sr
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
import feedparser

# === Inicializar pyttsx3 ===
engine = pyttsx3.init()
engine.setProperty('rate', 170)
engine.setProperty('volume', 1.0)
engine.setProperty('voice', engine.getProperty('voices')[0].id)  # Puedes cambiar el índice si deseas otra voz

def speak(text):
    print(f"Luna: {text}")
    engine.say(text)
    engine.runAndWait()

def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎙️ Di algo...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    try:
        return recognizer.recognize_google(audio, language="es-ES")
    except sr.UnknownValueError:
        speak("No entendí lo que dijiste.")
    except sr.RequestError:
        speak("Error de conexión con el servicio de reconocimiento.")
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
    now = datetime.now()
    if tipo == "hora":
        return f"Es la hora {now.strftime('%H:%M')}."
    elif tipo == "fecha":
        return f"Hoy es {now.strftime('%A, %d de %B de %Y')}."

def responder_fecha_futura(momento):
    now = datetime.now()
    dias = 1 if momento == "mañana" else 2
    fecha = now + timedelta(days=dias)
    return f"{momento.capitalize()} será {fecha.strftime('%A, %d de %B de %Y')}."

def responder_dias_semana(dia):
    hoy = datetime.now()
    dias = {"lunes": 0, "martes": 1, "miércoles": 2, "jueves": 3, "viernes": 4, "sábado": 5, "domingo": 6}
    dia_objetivo = dias.get(dia.lower())
    if dia_objetivo is None:
        return "No entendí qué día mencionaste."
    diferencia = (dia_objetivo - hoy.weekday()) % 7
    fecha = hoy + timedelta(days=diferencia)
    return f"El próximo {dia} será {fecha.strftime('%A, %d de %B de %Y')}."

def dias_faltantes_para_fecha(texto):
    match = re.search(r'(\d{1,2})\s+de\s+(enero|febrero|marzo|abril|mayo|junio|julio|agosto|septiembre|octubre|noviembre|diciembre)', texto.lower())
    if not match:
        return "No pude entender la fecha que mencionaste."
    dia = int(match.group(1))
    mes = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"].index(match.group(2)) + 1
    hoy = datetime.now()
    fecha_obj = datetime(hoy.year, mes, dia)
    if hoy > fecha_obj:
        fecha_obj = datetime(hoy.year + 1, mes, dia)
    dias = (fecha_obj - hoy).days
    return f"Faltan {dias} días para el {fecha_obj.strftime('%d de %B de %Y')}."

def obtener_noticias():
    url = "https://news.google.com/rss?hl=es-419&gl=PE&ceid=PE:es"
    noticias = feedparser.parse(url)
    if not noticias.entries:
        return "No se encontraron noticias."
    resultado = ""
    fuentes_usadas = set()
    contador = 0
    for entrada in noticias.entries:
        fuente = entrada.get("source", {}).get("title", "Fuente desconocida")
        if fuente in fuentes_usadas:
            continue
        resumen = BeautifulSoup(entrada.summary, "html.parser").get_text().strip()
        contador += 1
        resultado += f"{resumen} (Fuente: {fuente}).\n"
        fuentes_usadas.add(fuente)
        if contador == 5:
            break
    if contador == 0:
        return "No se encontraron noticias únicas de diferentes fuentes."
    return resultado.strip()

def consultar_clima(ciudad="Lima"):
    try:
        response = requests.get(f"https://wttr.in/{ciudad}?format=3", timeout=5)
        if response.ok:
            return response.text
        else:
            return "No se pudo obtener el clima en este momento."
    except Exception:
        return "No se pudo acceder al servicio del clima."

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
            speak("Hubo un error al contactar con el modelo.")
    except requests.exceptions.Timeout:
        speak("La solicitud tardó demasiado en responder.")
    except Exception as e:
        speak(f"Error de conexión: {e}")

def main():
    speak("Hola, soy Luna. ¿En qué puedo ayudarte?")
    while True:
        user_input = listen()
        if not user_input:
            continue
        if "salir" in user_input.lower():
            speak("Adiós, hasta pronto.")
            break
        tipo = detectar_pregunta_local(user_input)
        if tipo == "hora" or tipo == "fecha":
            speak(responder_pregunta_local(tipo))
        elif tipo == "futuro":
            if "pasado mañana" in user_input:
                speak(responder_fecha_futura("pasado mañana"))
            else:
                speak(responder_fecha_futura("mañana"))
        elif tipo == "dias_semana":
            for d in ["lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"]:
                if d in user_input.lower():
                    speak(responder_dias_semana(d))
                    break
        elif tipo == "falta_fecha":
            speak(dias_faltantes_para_fecha(user_input))
        elif tipo == "noticias":
            speak(obtener_noticias())
        elif tipo == "clima":
            speak(consultar_clima())
        else:
            print("Luna está procesando tu solicitud con el modelo de lenguaje.")
            ask_ollama_streaming(user_input)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        speak(f"Ocurrió un error inesperado: {e}")


