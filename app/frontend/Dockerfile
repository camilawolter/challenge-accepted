# Imagem base do Node.js
FROM node:16.14-alpine

# Diretório de trabalho dentro do contêiner
WORKDIR /app-frontend

# Copia do arquivo package.json para o diretório de trabalho
COPY package.json .
COPY package-lock.json .

# Instalando as dependências
RUN npm install

# Copia de todos os arquivos do projeto para o diretório de trabalho
COPY . .

# Porta que o aplicativo irá usar
EXPOSE 3000

# Comando para iniciar o aplicativo
CMD ["npm", "start"]
