#!/bin/bash

# Salir inmediatamente si un comando falla
set -o errexit

# Instalar Node.js y npm
curl -sL https://deb.nodesource.com/setup_14.x | bash -
apt-get install -y nodejs

# Verificar instalación de Node y npm
node -v
npm -v

# Instalar dependencias de Python
pip install -r requirements.txt

# Ejecutar colecta de archivos estáticos
python manage.py collectstatic --no-input

# Ejecutar migraciones
python manage.py migrate

# Construir Tailwind
python manage.py tailwind build
