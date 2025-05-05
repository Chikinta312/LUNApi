#!/bin/bash

# Actualización de repositorios y paquetes del sistema
echo "Actualizando los repositorios y paquetes del sistema..."
sudo apt-get update -y

# Instalación de dependencias del sistema
echo "Instalando dependencias necesarias..."
sudo apt-get install -y python3-pip python3-dev python3-setuptools build-essential \
libasound2-dev libjack-dev libsndfile1 libsndfile1-dev portaudio19-dev \
ffmpeg libatlas-base-dev libsox-fmt-all espeak libportaudio2 \
libcurl4-openssl-dev libssl-dev

# Instalación de las librerías necesarias para Python
echo "Instalando librerías necesarias para Python..."
pip3 install -r requirements.txt

# Verificación de instalación
echo "Verificando la instalación de las librerías..."
pip3 list

# Fin de la instalación
echo "Instalación completa. ¡Todo listo para usar el asistente Luna!"
