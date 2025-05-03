import os
import queue
import sounddevice as sd
import vosk
import pyttsx3
from llama_cpp import Llama

# === CONFIGURACIÓN ===
NOMBRE_ACTIVACION = "luna"
modelo_vosk = "modelos/vosk"
modelo_llama = "modelos/TinyLlama-1.1B-Chat-v1.0.Q4_K_M.gguf"

# Inicializar TTS
tts = pyttsx3.init()
def hablar(texto):
    tts.say(texto)
    tts.runAndWait()

# Inicializar modelo de voz (Vosk)
if not os.path.exists(modelo_vosk):
    print("Modelo Vosk no encontrado")
    exit(1)
vosk.SetLogLevel(-1)
model = vosk.Model(modelo_vosk)
q = queue.Queue()

def callback(indata, frames, time, status):
    if status:
        print(status, flush=True)
    q.put(bytes(indata))

# Inicializar modelo LLaMA
llm = Llama(model_path=modelo_llama, n_ctx=2048)

def responder(texto):
    prompt = f"[INST] {texto} [/INST]"
    respuesta = llm(prompt, max_tokens=256, stop=["</s>"])
    texto_respuesta = respuesta["choices"][0]["text"]
    print("LUNA:", texto_respuesta)
    hablar(texto_respuesta.strip())

# === Loop principal ===
def escuchar():
    with sd.RawInputStream(samplerate=16000, blocksize=8000, dtype='int16',
                           channels=1, callback=callback):
        print("Esperando el comando de activación 'Luna'...")
        rec = vosk.KaldiRecognizer(model, 16000)
        while True:
            data = q.get()
            if rec.AcceptWaveform(data):
                resultado = rec.Result()
                texto = eval(resultado)["text"]
                print("Escuchado:", texto)
                if NOMBRE_ACTIVACION in texto.lower():
                    hablar("¿En qué puedo ayudarte?")
                    print("Luna activada. Escuchando instrucción...")
                    instruccion = ""
                    while True:
                        data = q.get()
                        if rec.AcceptWaveform(data):
                            resultado = rec.Result()
                            instruccion = eval(resultado)["text"]
                            if instruccion:
                                print("Instrucción:", instruccion)
                                responder(instruccion)
                                print("Esperando el comando de activación 'Luna'...")
                                break

if __name__ == "__main__":
    escuchar()