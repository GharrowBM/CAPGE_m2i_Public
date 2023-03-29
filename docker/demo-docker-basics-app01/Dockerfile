FROM node:alpine

WORKDIR /app

COPY package.json .

RUN npm install
# RUN va exécuter une commande dans le terminal lors de la création de l'image Docker et non lors de la création du conteneur comme le ferait CMD

COPY . .

EXPOSE 80
# EXPOSE sert à avertir qu'un port va être utilisé par le conteneur, dans le but de permettre à l'utilisateur de notre image de savoir qu'un port peut être utilisé / mappé lors du lancement du conteneur

CMD [ "node", "server.js"]