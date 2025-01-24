FROM alpine:3.18
ENV NODE_VERSION=18.0.1

# Install necessary dependencies
RUN apk add --no-cache \
    curl \
    bash \
    libc6-compat \
    libstdc++ \
    libgcc \
    python3 \
    make \
    g++

# Install Node.js from the official distribution
ARG NODE_VERSION
RUN curl -fsSL https://nodejs.org/dist/v${NODE_VERSION}/node-v${NODE_VERSION}-linux-x64.tar.gz | tar -xz -C /usr/local --strip-components=1 \
    && ln -s /usr/local/bin/node /usr/bin/node \
    && ln -s /usr/local/bin/npm /usr/bin/npm \
    && ln -s /usr/local/bin/npx /usr/bin/npx

# Verify Node.js installation
RUN node -v && npm -v

# Set working directory
WORKDIR /app

# Copy application files and install dependencies
COPY package*.json ./
RUN npm install

# Copy application source code
COPY . .

# Expose application port (if needed)
EXPOSE 3000

# Start the application
CMD ["node", "index.js"]
