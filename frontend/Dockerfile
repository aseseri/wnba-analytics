# frontend/Dockerfile

# --- Stage 1: "base" ---
FROM node:18 AS base
WORKDIR /app
COPY package*.json ./
RUN npm ci

# --- Stage 2: "development" ---
FROM base AS development
COPY . .
CMD ["npm", "start"]

# --- Stage 3: "builder" ---
FROM base AS builder
COPY . .
# 1. Declare an argument that can be passed in during the build
ARG REACT_APP_API_BASE_URL
# 2. Set it as an environment variable *for this stage only*
ENV REACT_APP_API_BASE_URL=$REACT_APP_API_BASE_URL
RUN npm run build

# --- Stage 4: "production" ---
FROM nginx:stable-alpine AS production

# Install `envsubst` utility
RUN apk add --no-cache gettext

# Copy our Nginx config template into the image
COPY --from=builder /app/nginx/nginx.conf.template /etc/nginx/templates/nginx.conf.template

# Copy the built React app from the 'builder' stage
COPY --from=builder /app/build /usr/share/nginx/html

# The CMD now does two things:
# 1. Runs envsubst to substitute the $PORT variable into our template, creating the final config.
# 2. Starts the Nginx server.
CMD ["/bin/sh", "-c", "envsubst '${PORT}' < /etc/nginx/templates/nginx.conf.template > /etc/nginx/conf.d/default.conf && nginx -g 'daemon off;'"]