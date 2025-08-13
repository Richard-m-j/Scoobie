# ---- Stage 1: Build the React App ----
FROM node:18-alpine AS build

WORKDIR /app

COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build


# ---- Stage 2: Serve the App with Nginx ----
FROM nginx:1.25-alpine

# Copy the static files from the build stage
COPY --from=build /app/build /usr/share/nginx/html

# ADD THIS LINE: Copy our custom Nginx configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Expose the default Nginx port
EXPOSE 80

# The default Nginx command will start the server
CMD ["nginx", "-g", "daemon off;"]