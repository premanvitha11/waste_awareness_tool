# Frontend Dockerfile
FROM node:18-alpine

WORKDIR /app

# Copy package files
COPY frontend/package*.json ./

# Install dependencies
RUN npm ci

# Copy source code
COPY frontend/ .

# Build the app
RUN npm run build

# Serve with node
RUN npm install -g serve

EXPOSE 3000

CMD ["serve", "-s", "build"]
