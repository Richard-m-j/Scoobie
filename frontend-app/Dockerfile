# ---- Stage 1: Build the React App ----
FROM node:18-alpine AS build

# Set the working directory
WORKDIR /app

# Copy package.json and package-lock.json to leverage Docker cache
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of the application files
COPY . .

# Build the application for production
RUN npm run build


# ---- Stage 2: Serve the App with Nginx ----
FROM nginx:1.25-alpine

# Copy the static files from the build stage
COPY --from=build /app/build /usr/share/nginx/html

# Nginx listens on port 80 by default, so we expose it
EXPOSE 80

# The default Nginx command will start the server automatically
CMD ["nginx", "-g", "daemon off;"]