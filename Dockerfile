# Usa una imagen base de Python
FROM python:3.11

# Instala Node.js (versión recomendada) y npm
RUN curl -fsSL https://deb.nodesource.com/setup_18.x | bash - \
    && apt-get install -y nodejs \
    && npm install -g npm

# Establece el directorio de trabajo
WORKDIR /app

# Copia los archivos del proyecto al contenedor
COPY . /app/

# Instala las dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Instala las dependencias de Node.js (si hay package.json)
RUN npm install

# Ejecuta colecta de archivos estáticos
RUN python manage.py collectstatic --no-input

# Ejecuta migraciones
RUN python manage.py migrate

# Construye Tailwind
RUN python manage.py tailwind build

# Exponer el puerto (cambia el puerto según tu configuración)
EXPOSE 8000

# Comando para ejecutar la aplicación
CMD ["gunicorn", "generalApp.wsgi:application", "--bind", "0.0.0.0:8000"]
