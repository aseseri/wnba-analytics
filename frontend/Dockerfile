# frontend/Dockerfile

# --- Stage 1: Development ---
FROM node:18 AS development
WORKDIR /app

# Copy package.json first to leverage Docker layer caching
COPY package*.json ./
RUN npm install

# Copy the rest of the application code
COPY . .

# The default command to run when this stage is started
# This starts the React Development Server with hot-reloading
CMD ["npm", "start"]

# --- Stage 2: Production ---
# This stage is now clearly separated and will only be used for production builds later
# Serve the built app with a lightweight web server
FROM nginx:stable-alpine as production
# Copy the built files from the 'development' stage
COPY --from=development /app/build /usr/share/nginx/html
# Expose port 80, which is the default for NGINX
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]