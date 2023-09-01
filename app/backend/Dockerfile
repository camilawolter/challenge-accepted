# Imagem Python oficial como base
FROM python:3.8

# Diretório de trabalho dentro do contêiner
WORKDIR /app-backend

# Copia do arquivo requirements.txt para o diretório de trabalho
COPY requirements.txt .

# Instalando as dependências do projeto
RUN pip install -r requirements.txt

# Copia de todos os arquivos do projeto para o diretório de trabalho
COPY . .

# Porta em que o servidor do back-end será executado 
EXPOSE 8000

# Comando para iniciar o servidor Python 
CMD ["python", "app.py"]
