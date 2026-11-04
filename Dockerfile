# Etapa 1: gera o site estático
FROM python:3.12-slim AS build
WORKDIR /docs
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN mkdocs build --strict

# Etapa 2: serve com Nginx
FROM nginx:alpine
COPY --from=build /docs/site /usr/share/nginx/html
EXPOSE 80
