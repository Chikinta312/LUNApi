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
engine.setProperty('rate', 170)  # Velocidad de habla
engine.setProperty('volume', 1.0)  # Volumen máximo
engine.setProperty('voice', engine.getProperty('voices')[0].id)  # Voz en español

def speak(text):
    """Función para que el asistente hable."""
    print(f"Luna: {text}")
    engine.say(text)
    engine.runAndWait()

def listen():
    """Función para escuchar la voz del usuario."""
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
        speak("Error de conexión con el servicio de reconocimiento.")
        return ""

def detectar_pregunta_local(texto):
    """Detecta qué tipo de pregunta hace el usuario."""
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
    """Responde preguntas locales como hora o fecha."""
    ahora = datetime.now()
    if tipo == "hora":
        return f"Son las {ahora.strftime('%H:%M')}."
    elif tipo == "fecha":
        return f"Hoy es {ahora.strftime('%A, %d de %B de %Y')}."

def responder_fecha_futura(momento):
    """Responde sobre fechas futuras como 'mañana' o 'pasado mañana'."""
    ahora = datetime.now()
    dias = 1 if momento == "mañana" else 2
    fecha = ahora + timedelta(dias=dias)
    return f"{momento.capitalize()} será {fecha.strftime('%A, %d de %B de %Y')}."

def responder_dias_semana(dia):
    """Responde con la fecha del próximo día de la semana solicitado."""
    hoy = datetime.now()
    dias = {"lunes": 0, "martes": 1, "miércoles": 2, "jueves": 3, "viernes": 4, "sábado": 5, "domingo": 6}
    dia_objetivo = dias.get(dia.lower())
    if dia_objetivo is None:
        return "No entendí qué día mencionaste."
    diferencia = (dia_objetivo - hoy.weekday()) % 7
    fecha = hoy + timedelta(dias=diferencia)
    return f"El próximo {dia} será {fecha.strftime('%A, %d de %B de %Y')}."

def dias_faltantes_para_fecha(texto):
    """Calcula cuántos días faltan hasta una fecha específica."""
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
    """Obtiene las últimas 5 noticias de Google News RSS, con un titular por fuente."""
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
        
        # Obtener solo el titular de la noticia
        titular = BeautifulSoup(entrada.title, "html.parser").get_text().strip()
        
        # Añadir la noticia al resultado, sin repetir la fuente
        if contador == 0:
            resultado += f"{titular} (Fuente: {fuente})"
        else:
            resultado += f"\n{titular} (Fuente: {fuente})"
        
        # Marcar la fuente como usada
        fuentes_usadas.add(fuente)
        
        # Limitar a 5 noticias
        contador += 1
        if contador == 5:
            break

    if contador == 0:
        return "No se encontraron noticias únicas de diferentes fuentes."
    
    return resultado.strip()

def consultar_clima(ciudad="Lima"):
    """Consulta el clima actual de la ciudad dada."""
    try:
        response = requests.get(f"https://wttr.in/{ciudad}?format=3", timeout=5)
        if response.ok:
            return response.text
        else:
            return "No se pudo obtener el clima en este momento."
    except Exception:
        return "No se pudo acceder al servicio del clima."

def ask_ollama_streaming(prompt):
    """Consultas el modelo Gemma3 1B para obtener respuestas dinámicas."""
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
    """Función principal donde el asistente escucha y responde a los comandos del usuario."""
    speak("Hola, soy Luna. Di 'Luna' seguido de tu solicitud para comenzar.")
    while True:
        user_input = listen()
        if not user_input:
            continue
        user_input = user_input.lower()
        if not user_input.startswith("luna"):
            continue

        comando = user_input[4:].strip()

        if "salir" in comando:
            speak("Adiós, hasta pronto.")
            break

        tipo = detectar_pregunta_local(comando)

        if tipo == "hora" or tipo == "fecha":
            speak(responder_pregunta_local(tipo))
        elif tipo == "futuro":
            if "pasado mañana" in comando:
                speak(responder_fecha_futura("pasado mañana"))
            else:
                speak(responder_fecha_futura("mañana"))
        elif tipo == "dias_semana":
            for d in ["lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"]:
                if d in comando:
                    speak(responder_dias_semana(d))
                    break
        elif tipo == "falta_fecha":
            speak(dias_faltantes_para_fecha(comando))
        elif tipo == "noticias":
            speak(obtener_noticias())
        elif tipo == "clima":
            speak(consultar_clima())
        else:
            print("Luna está procesando tu solicitud con el modelo de lenguaje.")
            ask_ollama_streaming(comando)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        speak(f"Ocurrió un error inesperado: {e}")


