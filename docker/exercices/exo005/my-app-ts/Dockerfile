# Base image
FROM node:alpine

# Set working directory
WORKDIR /app

# Copy package.json and package-lock.json
COPY package.json .

# Install dependencies
RUN npm install

# Copy app files
COPY . .

# Build the React app
RUN npm run build

# Set the start command
CMD ["npm", "start"]
