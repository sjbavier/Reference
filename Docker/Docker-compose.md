# Working with Docker Compose CLI

## Docker compose is used to define and run multi-container applications with Docker [https://docs.docker.com/compose/reference/overview/] 

Working with yaml config[s] is the recommended way to scaffold applications

```sh
docker-compose -f <file-yml>
```

example yaml

```yaml
version: '2'

services:  
  # the `extends` command references the `web` service in our
  # file is the relative path to the extended definition of the service
  # the command in this file.
  web:
    extends:
      file: <relative-yaml-path>
      service: web
    command: yarn start

  story:
    extends:
      file: <relative-yaml-path>
      service: story
    command: yarn run storybook

  sass:
    extends:
      file: <relative-yaml-path>
      service: sass
    command: sass --watch /usr/src/app/src:/usr/src/app/src
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

Stream container events for every service

```sh
docker-compose events
```

Show a list of of containers for a service

```sh
docker-compose ps
```

Display compose configuration and check for validity

```sh
docker-compose config
```

Push and pull images associated with services defined in yaml file(s)

```sh
docker-compose pull
docker-compose push
```

Build or rebuild services

```sh
docker-compose build
```

Shutdown the containers, networks, images and volumes

```sh
docker-compose down # command has to be executed in the directory of the docker-compose.yml file
```
