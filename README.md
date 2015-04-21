# Plano



To launch the API you just have to execute `docker-compose`

```
$ docker-compose up
```

If you don't have docker compose or you like to know a bit better which components are used and how do they link together, use the following commands:

```
docker build -t plano .
docker run --name mongodb -d mongo
docker run --name neo4j -p 7474:7474 tpires/neo4j
docker run -it --link mongodb:mongodb --link neo4j:neo4j -p 5000:5000 -v $(pwd):/app plano
```

If you need to access the MongoDB, use the following command:

```
docker run -it --link python_mongodb_1:mongo --rm mongo sh -c 'exec mongo "$MONGO_PORT_27017_TCP_ADDR:$MONGO_PORT_27017_TCP_PORT/test"'

```

The API allows to define entities like Application, Components and Runtimes and create relationships between them.

You can access the [Neo4j browser](https://localhost:7474) to see the different results.

Plano allows you to define your architecture. You can upload `docker-compose` yaml files and it will map the application.

### TODO:

* support for AWS Cloudformation
