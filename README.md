# Actividad 1 - Hardening de MongoDB, Elasticsearch y FastAPI

## Autor

Alberto Villar Rodríguez

## Descripción

Laboratorio de ciberseguridad para la identificación y mitigación de vulnerabilidades en:

- MongoDB sin autenticación.
- Elasticsearch sin mecanismos de seguridad.
- API FastAPI vulnerable a NoSQL Injection.

El objetivo es demostrar las vulnerabilidades, aplicar contramedidas y verificar su mitigación.

---

## Tecnologías utilizadas

- Docker
- Docker Compose
- Python 3.11
- FastAPI
- MongoDB 7
- Elasticsearch 7.17.10

---

## Estructura del proyecto

```text
Actividad1/
├── docker-compose.yml
├── init_mongo.js
├── README.md
└── fastapi-app/
    ├── Dockerfile
    ├── requirements.txt
    └── main.py
```

---

## Requisitos

Instalar:

- Docker Engine
- Docker Compose

Comprobar instalación:

```bash
docker --version
docker compose version
```

---

## Despliegue del entorno

Construir y arrancar los contenedores:

```bash
docker compose up -d --build
```

Comprobar que los servicios están activos:

```bash
docker ps
```

Deberán aparecer:

- MongoDB
- Elasticsearch
- FastAPI

---

## Reinicio completo del laboratorio

Eliminar contenedores y datos:

```bash
docker compose down -v
```

Reconstruir el entorno:

```bash
docker compose up -d --build
```

---

## Acceso a los servicios

### FastAPI

Documentación Swagger:

```text
http://localhost:8000/docs
```

### Elasticsearch

API REST:

```text
http://localhost:9200
```

### MongoDB

```text
localhost:27017
```

---

## Datos de prueba

### Usuarios

| Usuario | Contraseña |
|----------|------------|
| alberto | 1234 |
| villar | abcd |

### Pedidos

| Producto | Cantidad |
|-----------|-----------|
| Portatil Lenovo | 1 |
| Monitor Dell | 2 |

---

## Pruebas de funcionamiento

### Login legítimo

```bash
curl -X POST http://localhost:8000/login_mongo \
-H "Content-Type: application/json" \
-d '{"username":"alberto","password":"1234"}'
```

Respuesta esperada:

```json
{"msg":"ok"}
```

---

### Creación de pedido

```bash
curl -X POST http://localhost:8000/pedidos \
-H "Content-Type: application/json" \
-d '{
  "producto":"Teclado Logitech",
  "cantidad":1
}'
```

---

### Consulta de pedidos

```bash
curl http://localhost:8000/pedidos
```

---

### Consulta de artículos

```bash
curl "http://localhost:8000/articulos?q=*"
```

---

## Vulnerabilidades demostradas

### NoSQL Injection

```bash
curl -X POST http://localhost:8000/login_mongo \
-H "Content-Type: application/json" \
-d '{"username":"alberto","password":{"$ne":"x"}}'
```

---

### MongoDB sin autenticación

Conexión directa mediante:

```bash
mongosh
```

Sin necesidad de usuario ni contraseña.

---

### Elasticsearch expuesto

Enumeración de índices:

```bash
curl http://localhost:9200/_cat/indices?v
```

Consulta de documentos:

```bash
curl "http://localhost:9200/articulos/_search?q=*"
```

Eliminación de índices:

```bash
curl -X DELETE http://localhost:9200/articulos
```

---

## Contramedidas implementadas

- Validación de entradas mediante Pydantic.
- Prevención de NoSQL Injection.
- Activación de autenticación en MongoDB.
- Restricción de acceso a Elasticsearch.
- Aplicación de la paginación en la búsqueda de resultados
- Rate limit para el login
- Documentación de intentos de login fallidos

---

## Referencias

- MongoDB Documentation
- Elastic Documentation
- FastAPI Documentation
- OWASP NoSQL Injection
