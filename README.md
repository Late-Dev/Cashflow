# Cashflow
Cashflow telegram bot

## How to run

1. Create ```.env``` file

Example
```
POSTGRES_USER=admin
POSTGRES_PASSWORD=admin

PGADMIN_DEFAULT_EMAIL=admin@admin.com
PGADMIN_DEFAULT_PASSWORD=root

TOKEN=<your telegram token>
SECRET_KEY=<your secret_key>
```

2. Run ```docker compose --env-file .env up```

## Database schema

![schema](schema.svg)

## Services

swagger - http://localhost:8000/docs

pgadmin4 - http://localhost:5050/
