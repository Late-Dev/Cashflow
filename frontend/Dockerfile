FROM oven/bun:latest AS build

RUN bun install -g http-server
WORKDIR /app

COPY package.json ./
COPY bun.lockb ./

RUN bun install
COPY . ./
RUN bun install
RUN bun run build


FROM nginx:1.19.0 AS serve
WORKDIR /usr/share/nginx/html
COPY --from=build /app/dist ./

EXPOSE 80

