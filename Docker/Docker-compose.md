# Working with Docker Compose CLI

## Docker compose is used to define and run multi-container applications with Docker

Working with yaml config[s] is the recommended way to scaffold applications

```sh
docker-compose -f <file-yml>
```

You can also run commands within a service

```sh
docker-compose -f <file-yml> run <service> <cmd-run-in-working-dir>
```

Run a shell inside of a particular service

```sh
docker-compose run <service> bash
```

To create and start containers

```sh
docker-compose up -d # -d for detached
```

Watch the logs of the containers

```sh
docker-compose logs -f # -f for follow
```

Shutdown the containers, networks, images and volumes

```sh
docker-compose down # command has to be executed in the directory of the docker-compose.yml file
```
