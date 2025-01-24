ARG NODE_VERSION
FROM node:${NODE_VERSION}-alpine

# Optional: Add metadata
LABEL maintainer="devops"

# Optional: Set a working directory
WORKDIR /app

# Optional: Copy files and install dependencies (if needed)
COPY package*.json ./
RUN npm install

# Optional: Copy application source
COPY . .

CMD ["node"]
