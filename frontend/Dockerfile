# frontend/Dockerfile

# Stage 1: Build the React app
FROM node:18 AS build
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

# Stage 2: Serve the built app with a lightweight web server
FROM nginx:stable-alpine
COPY --from=build /app/build /usr/share/nginx/html
# Expose port 80, which is the default for NGINX
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]