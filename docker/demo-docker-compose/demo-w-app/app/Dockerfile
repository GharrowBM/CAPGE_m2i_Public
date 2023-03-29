FROM node:alpine

WORKDIR /app

COPY package.json .

RUN npm install 

COPY . .

ENV LISTENING_PORT=3000

EXPOSE ${LISTENING_PORT}

# VOLUME [ "/app/feedback" ]

CMD [ "npm", "start" ]