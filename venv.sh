#!/bin/bash

# Ruta a la carpeta del entorno virtual
VENV_DIR=".venv"

# Verifica si la carpeta del entorno virtual existe
if [ -d "$VENV_DIR" ]; then
    # Activa el entorno virtual
    source "$VENV_DIR/bin/activate"
    echo "Entorno virtual activado."
else
    echo "La carpeta del entorno virtual $VENV_DIR no existe. Asegúrate de configurar tu entorno virtual correctamente."
fi