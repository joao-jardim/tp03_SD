# Usar uma imagem base do Python
FROM python:3.9-slim

# Copiar o script para o container
COPY script.py /app/script.py
COPY Functions.py /app/Functions.py

# Definir o diretório de trabalho
WORKDIR /app

# Comando para executar o script
CMD ["python", "script.py"]
