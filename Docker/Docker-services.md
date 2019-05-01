# Working with Docker Services

The **docker-compose.yml** file used to define run and scale services with the Docker platform. Place this file wherever you want, however you must have pushed the docker image

```Dockerfile

version: "3"
services:
  web:
    # replace username/repo:tag with your name and image details
    image: username/repo:tag
    deploy:
        # run 5 instances
      replicas: 5 
      resources:
        limits:
        # limit each to use at most 10% of the CPU (across all cores) and 50MB of RAM
          cpus: "0.1"
          memory: 50M
      restart_policy:
        # Immediately restart failed containers
        condition: on-failure
    ports:
        # map port 4000 on host to containerized service's 'web' port 80
      - "4000:80"
    networks:
        # instruct 'web' containers to share port 80 via a load-balanced(default) network called 'webnet' (internally the containers themselves publish to 'web' port 80 at an ephemeral port)
      - webnet
networks:
  webnet:

```

To run your new load-balanced app first run (to initiate swarm manager)

```sh
docker swarm init
```

Second to name and deploy the app (also can be used to re-deploy if you have added replicas)

```sh
docker stack deploy -c docker-compose.yml nameOfApp
```

List service

```sh
docker service ls
```

A single container running a service is called a task (given unique IDs that numerically increment based on 'replicas' defined in your docker-compose.yml). Lists the tasks for the service

```sh
docker service ps <service_name>
```

Listing all containers

```sh
docker container ls -q
```

Take down the app

```sh
docker stack rm nameOfApp
```

Take down the swarm

```sh
docker swarm leave --force
```

cheatsheet recap

```sh
docker stack ls                                            # List stacks or apps
docker stack deploy -c <composefile> <appname>  # Run the specified Compose file
docker service ls                 # List running services associated with an app
docker service ps <service>                  # List tasks associated with an app
docker inspect <task or container>                   # Inspect task or container
docker container ls -q                                      # List container IDs
docker stack rm <appname>                             # Tear down an application
docker swarm leave --force      # Take down a single node swarm from the manager
```