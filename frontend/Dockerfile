FROM node:18 AS build

WORKDIR /app

COPY ./frontend/package.json ./frontend/yarn.lock ./
COPY .env ./
COPY ./frontend ./

RUN yarn install
RUN yarn run build


FROM nginx:1.19.0 AS serve
WORKDIR /usr/share/nginx/html
COPY --from=build /app/dist/spa ./

EXPOSE 80

