# Imagem Python oficial como base 
FROM python:3.11-slim 
# Permite que mensagens de erro apareçam imediatamente 
ENV PYTHONUNBUFFERED True 
# Define diretório dentro do contéiner
WORKDIR /app-backend
# Copia do arquivo requirements.txt para o diretório de trabalho 
COPY requirements.txt . 
## Instalando as dependências do projeto 
RUN pip install --no-cache-dir -r requirements.txt
# Copia de todos os arquivos do projeto para o diretório de trabalho 
COPY . . 
# Porta em que o servidor do back-end será executado  
EXPOSE 5000 
## Comando para iniciar o servidor Python  
CMD exec gunicorn --bind :5000 --workers 1 --threads 8 --timeout 0 main:app
