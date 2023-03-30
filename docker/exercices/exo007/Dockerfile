FROM node

RUN mkdir -p /app/uploads

WORKDIR /app

COPY package.json .

RUN npm install 

COPY . .

VOLUME [ "/app/uploads" ]

CMD ["node", "/app/app.js"]