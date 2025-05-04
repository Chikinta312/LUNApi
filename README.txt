
# Asistente Virtual Luna en Raspberry Pi 5B

**Luna** es un asistente virtual de código abierto diseñado para ejecutarse de manera local en una Raspberry Pi 5B, que utiliza el sistema operativo Raspbian 64 bits. Este asistente está basado en la integración de varias librerías y herramientas, incluyendo **OMALLA** y su modelo de lenguaje **Gemma3**, para proporcionar respuestas a preguntas sobre el clima, noticias, hora, fecha, eventos y más. Además, **Luna** puede entender comandos de voz y responder de forma natural.

## Requisitos

### Hardware:

* Raspberry Pi 5B (minimo de 4 gb ram para poder usar solo el Gemma3:1b)
* Micrófono y altavoces conectados a la Raspberry Pi

### Software:

* Raspbian 64 bits (o cualquier sistema operativo basado en Debian)
* Python 3.x
* OMALLA instalado en la Raspberry Pi
* Librerías de Python requeridas

## Instalación

### 1. Instalación de Raspbian

Instala **Raspbian 64 bits** en tu Raspberry Pi siguiendo las instrucciones en [la página oficial de Raspberry Pi](https://www.raspberrypi.org/software/).

### 2. Instalación de OMALLA

OMALLA es el servicio que permite la integración con el modelo de lenguaje **Gemma3**. Para instalar OMALLA, sigue estos pasos:

1. Abre una terminal en tu Raspberry Pi.
2. Instala OMALLA siguiendo las instrucciones de su repositorio oficial:

   * Ve al repositorio oficial de OMALLA y sigue las instrucciones de instalación.

> **Nota:** Asegúrate de que OMALLA esté ejecutándose correctamente y que el modelo **Gemma3** esté instalado antes de continuar.

### 3. Instalación de las librerías necesarias

Una vez que OMALLA esté instalado y funcionando, procede a instalar las librerías necesarias para el asistente.

Ejecuta el siguiente comando en la terminal para instalar las dependencias de Python:

```bash
pip install -r requirements.txt
```

El archivo `requirements.txt` debe contener las siguientes librerías:

```text
speechrecognition
pyttsx3
requests
json
re
beautifulsoup4
feedparser
winsound
```

### 4. Configuración de OMALLA

Asegúrate de que OMALLA esté configurado y ejecutándose en tu Raspberry Pi en el puerto **11434** (puerto predeterminado). Puedes verificar que OMALLA está funcionando correctamente haciendo una solicitud al endpoint:

```bash
curl http://localhost:11434/api/generate
```

Deberías recibir una respuesta JSON en formato de flujo.

### 5. Colocar el asistente como función de arranque

Para que **Luna** se ejecute automáticamente cuando inicie la Raspberry Pi, debes configurar el script en el inicio del sistema.

1. Abre la terminal.
2. Abre el archivo `rc.local` para editarlo:

```bash
sudo nano /etc/rc.local
```

3. Agrega la siguiente línea antes de la línea `exit 0`:

```bash
python3 /ruta/a/tu/archivo/luna.py &
```

> **Nota:** Asegúrate de reemplazar `/ruta/a/tu/archivo/luna.py` con la ruta completa al archivo del script de **Luna**.

4. Guarda y cierra el archivo presionando **Ctrl + X**, luego **Y** y **Enter**.

Esto ejecutará el script de **Luna** automáticamente cuando inicie tu Raspberry Pi.

## Uso

Cuando la Raspberry Pi se inicie, **Luna** comenzará a escuchar en busca de comandos de voz. Puedes pedirle a Luna que:

* Te diga la **hora**.
* Te diga la **fecha**.
* Te informe sobre el **clima**.
* Te cuente las **noticias**.
* Te diga el **día de la semana** para un día específico.
* Te diga **cuánto falta** para una fecha.
* Responda preguntas generales utilizando **Gemma3** (a través de OMALLA).

### Comandos soportados:

* "¿Qué hora es?"
* "¿Cuál es la fecha de hoy?"
* "¿Cómo estará el clima en Lima?"
* "Dime las noticias"
* "¿Cuándo es el próximo lunes?"

### Salir del asistente:

Para salir del asistente, solo di "salir" y **Luna** se despedirá.

## Funciones Implementadas

### 1. **Reconocimiento de Voz:**

* Utiliza el micrófono para escuchar comandos y preguntas.
* El reconocimiento de voz se realiza mediante la librería **speech\_recognition**.

### 2. **Respuestas de Voz:**

* **Luna** responde mediante voz utilizando la librería **pyttsx3**.

### 3. **Consultas Locales:**

* Responde preguntas sobre **hora**, **fecha**, **días de la semana**, **eventos futuros**, y **clima**.
* Utiliza la API de **wttr.in** para obtener el clima de una ciudad.

### 4. **Noticias:**

* Obtiene las últimas noticias a través de RSS con **feedparser**.

### 5. **Interacción con OMALLA (Gemma3):**

* Si no se entiende la pregunta, **Luna** interactúa con el modelo **Gemma3** a través de OMALLA para dar respuestas más detalladas.

## Contribuciones

Si deseas contribuir al proyecto, siéntete libre de hacer un **fork** del repositorio y enviar tus **pull requests**. ¡Toda ayuda es bienvenida!

## Licencia

Este proyecto está bajo la licencia MIT. Puedes ver más detalles en el archivo `LICENSE`.

---

¡Espero que este `README.md` te sea útil para tu repositorio!
