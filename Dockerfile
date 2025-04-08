# Usar una imagen base con Python 3.11
FROM python:3.11-slim

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar los archivos del proyecto
COPY backend/requirements.txt .
COPY backend/api/ .

# Instalar las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Exponer el puerto y ejecutar la aplicación
CMD ["gunicorn", "app:app", "--workers", "1", "--threads", "4", "--timeout", "60"]