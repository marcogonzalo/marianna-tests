###################################################
# Stage: base
# 
# This base stage ensures all other stages are using the same base image
# and provides common configuration for all stages, such as the working dir.
###################################################
FROM node:22-alpine AS node-base
WORKDIR /usr/local/app

###################################################
# Stage: client-base
#
# This stage is used as the base for the client-dev and client-build stages,
# since there are common steps needed for each.
###################################################
FROM node-base AS client-base
COPY package*.json ./
RUN --mount=type=cache,id=npm,target=/root/.npm \
    npm install
COPY ./*.config.*s ./tsconfig*.json ./

###################################################
# Stage: client-dev
# 
# This stage is used for development of the client application. It sets 
# the default command to start the Vite development server.
###################################################
FROM client-base AS client-dev
EXPOSE 5173
CMD ["npm", "run", "dev"]

###################################################
# Stage: client-build
# 
# This stage builds the production assets.
###################################################
FROM client-base AS client-build
COPY . .
# Clean any previous builds and node_modules
RUN rm -rf dist node_modules/.vite node_modules/.tmp
# Install dependencies and build
RUN npm ci && \
    NODE_ENV=production VITE_TSCONFIG=tsconfig.prod.json npm run build

###################################################
# Stage: client-prod
# 
# This stage serves the production build using nginx.
###################################################
FROM nginx:1.25-alpine AS client-prod
COPY --from=client-build /usr/local/app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 5173
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5173/health || exit 1
