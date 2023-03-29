FROM node:alpine

WORKDIR /app

COPY package.json .

RUN npm install 

COPY . .

ARG DEFAULT_PORT=80

ENV LISTENING_PORT=${DEFAULT_PORT}

EXPOSE ${LISTENING_PORT}

# VOLUME [ "/app/feedback" ]

CMD [ "npm", "start" ]