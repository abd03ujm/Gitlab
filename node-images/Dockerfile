# Use official Node.js image as the base
FROM node:14
ENV NODE_VERSION 17.0.1
# Set the working directory in the container
WORKDIR /app

# Copy package.json and package-lock.json to the container
#COPY package*.json ./

# Install dependencies
#RUN npm install

# Copy the rest of the application files to the container
COPY . .

# Expose the application port
EXPOSE 3000

# Command to run the application
CMD ["npm", "start"]
