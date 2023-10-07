FROM node:18 AS build

WORKDIR /app

COPY package.json yarn.lock ./

RUN yarn install
COPY . ./
RUN yarn install
RUN yarn run build


FROM nginx:1.19.0 AS serve
WORKDIR /usr/share/nginx/html
COPY --from=build /app/dist ./

EXPOSE 80

