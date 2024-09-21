# Usar uma imagem Node.js para construir o projeto
FROM node:14 AS build

WORKDIR /app
COPY package.json ./
COPY package-lock.json ./
RUN npm install
COPY . .
RUN npm run build

# Usar uma imagem Nginx para servir o aplicativo
FROM nginx:alpine
COPY --from=build /app/build /usr/share/nginx/html
CMD ["nginx", "-g", "daemon off;"]
