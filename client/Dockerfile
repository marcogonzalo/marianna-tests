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
COPY ./package*.json ./
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
