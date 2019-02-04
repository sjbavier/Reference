## List Docker CLI commands
docker
docker container --help

## Display Docker version and info
docker --version
docker version
docker info

## Execute Docker image
docker run hello-world

## List Docker images
docker image ls

## List Docker containers (running, all, all in quiet mode)
docker container ls
docker container ls --all
docker container ls -aq

```Dockerfile
# Use an official Python runtime as a parent image
FROM python:2.7-slim

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 80

# Define environment variable
ENV NAME World

# Run app.py when the container launches
CMD ["python", "app.py"]
```


# Inside requirements.txt for example:

```Txt
Flask
Redis
```


# Make port 80 available to the world outside this container
EXPOSE 80

# Define environment variable
ENV NAME World

# Run app.py when the container launches
CMD ["python", "app.py"]

# Build the Docker image
docker build --tag=friendlyhello .

# Set proxy server, replace host:port with values for your servers
ENV http_proxy host:port
ENV https_proxy host:port

# To change the DNS specification settings in your Docker daemon (necessary for pip) /etc/docker/daemon.json

# The the second item is Google's DNS which can be use if the first is unavailable

```json
{
  "dns": ["your_dns_address", "8.8.8.8"]
}
```

# Running the app mapping machine's port 4000 to container's port 80 using flag 

```sh
docker run -p 4000:80 friendlyhello
```

# Can find ip address of "localhost" Docker Machine IP

```sh
docker-machine ip
```

# Run application in detached mode

```sh
docker run -d -p 4000:80 friendlyhello
```

# Listing containers

```sh
docker container ls

CONTAINER ID        IMAGE               COMMAND             CREATED
1fa4ab2cf395        friendlyhello       "python app.py"     28 seconds ago
```

# Stop containers using the container id

```sh
docker container stop 1fa4ab2cf395
```

# Log in to Docker registry (default is a public registry hub.docker.com)

```sh
docker login
```

# To associate local image with a repository on a registry.  The tag is optional which gives images a version

```sh
docker tag image username/repository:tag
```

# Example:

```sh
docker tag friendlyhello sjbavier/get-started:version2
```

# To see your tagged image

```sh
$ docker image ls
```

# Upload your tagged image to repository

```sh
docker push username/repository:tag
```

# Now you can run your image from any machine

```sh
docker run -p 4000:80 sjbavier/get-started:part2
```

# Recap 

```sh
docker build -t friendlyhello .  # Create image using this directory's Dockerfile
docker run -p 4000:80 friendlyhello  # Run "friendlyname" mapping port 4000 to 80
docker run -d -p 4000:80 friendlyhello         # Same thing, but in detached mode
docker container ls                                # List all running containers
docker container ls -a             # List all containers, even those not running
docker container stop <hash>           # Gracefully stop the specified container
docker container kill <hash>         # Force shutdown of the specified container
docker container rm <hash>        # Remove specified container from this machine
docker container rm $(docker container ls -a -q)         # Remove all containers
docker image ls -a                             # List all images on this machine
docker image rm <image id>            # Remove specified image from this machine
docker image rm $(docker image ls -a -q)   # Remove all images from this machine
docker login             # Log in this CLI session using your Docker credentials
docker tag <image> username/repository:tag  # Tag <image> for upload to registry
docker push username/repository:tag            # Upload tagged image to registry
docker run username/repository:tag                   # Run image from a registry
```

