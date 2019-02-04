<!-- Intro: A swarm is a group of machines running docker containing containers and joined into a cluster by a swarm manager who controls execution of commands and authentication of joining machines. -->

# To initiate swarm mode and make current machine a swarm manager

```sh
docker swarm init
```

# After running docker swarm init you will want to copy that pre-configured command that contains the token so you can easily command other machines to join the swarm

```sh
docker-machine ssh myvm2 "docker swarm join --token <token> <ip>:2377
```

# To have other virtual machines join as workers

```sh
docker swarm join
```

# To create docker machines on your local machine ( must first have VirtualBox for Linux or Hyper-V for Windows 10)

```sh
docker-machine create --driver virtualbox myvm1
```

# To list the docker-machine vms created with the VirtualBox driver

```sh
docker-machine ls
```

# To have the docker-machine become the swarm manager

```sh
docker-machine ssh myvm1 "docker-swarm init --advertise-addr <myvm1-ip>
```

# To add a worker to the swarm

```sh
docker swarm join \
--token <token> \
<myvm-ip>:<port>
```

# To add manager to a swarm

```sh
docker swarm join-token manager
```

# Always run docker swarm init and docker swarm join with port 2377.  Machine IP addresses returned by docker-machine ls include port 2376 which is the docker Daemon port, do not use this port.

# To use your own systems ssh ( can sometimes alleviate issues )

```sh
docker-machine --native-ssh ssh myvm1
```

# To view nodes on the swarm. Run this on the swarm manager

```sh
docker-machine ssh myvm1 "docker node ls"
```

# To have a node leave the swarm

```sh
docker swarm leave
```

# Another option instead of docker-machine ssh is to use env variables to talk to docker vm

```sh
docker-machine env myvm1

export DOCKER_TLS_VERIFY="1"
export DOCKER_HOST="tcp://192.168.99.100:2376"
export DOCKER_CERT_PATH="/Users/sam/.docker/machine/machines/myvm1"
export DOCKER_MACHINE_NAME="myvm1"
# Run this command to configure your shell:
# eval $(docker-machine env myvm1)
```

# To unset env in current shell

```sh
eval $(docker-machine env -u)
```

# Deploy your app on the swarm manager

```sh
docker stack deploy -c docker-compose.yml nameOfApp
```

# Note: if you store your image on a private registry you must be logged in using docker login and then use the --with-registry-auth 

```sh
docker login registry.example.com
docker stack deploy --with-registry-auth -c docker-compose.yml nameOfApp
```

# Now you can view your swarm

```sh
$ docker stack ps getstartedlab

ID            NAME                  IMAGE                   NODE   DESIRED STATE
jq2g3qp8nzwx  getstartedlab_web.1   gordon/get-started:part2  myvm1  Running
88wgshobzoxl  getstartedlab_web.2   gordon/get-started:part2  myvm2  Running
vbb1qbkb0o2z  getstartedlab_web.3   gordon/get-started:part2  myvm2  Running
ghii74p9budx  getstartedlab_web.4   gordon/get-started:part2  myvm1  Running
0prmarhavs87  getstartedlab_web.5   gordon/get-started:part2  myvm2  Running
```

# On mac and linux you may use scp to copy files to a machine

```sh
docker-machine scp <file> <machine>:~
```

# Keep in mind that inorder to use the ingress network in the swarm
Port 7946 TCP/UDP for container network discovery
Port 4789 UDP for container ingress network

# To tear down the stack

```sh
docker stack rm myAppName
```

# To restart a machine

```sh
docker-machine start myvm1
```

# Recap cheatsheet

```sh
docker-machine create --driver virtualbox myvm1 # Create a VM (Mac, Win7, Linux)
docker-machine create -d hyperv --hyperv-virtual-switch "myswitch" myvm1 # Win10
docker-machine env myvm1                # View basic information about your node
docker-machine ssh myvm1 "docker node ls"         # List the nodes in your swarm
docker-machine ssh myvm1 "docker node inspect <node ID>"        # Inspect a node
docker-machine ssh myvm1 "docker swarm join-token -q worker"   # View join token
docker-machine ssh myvm1   # Open an SSH session with the VM; type "exit" to end
docker node ls                # View nodes in swarm (while logged on to manager)
docker-machine ssh myvm2 "docker swarm leave"  # Make the worker leave the swarm
docker-machine ssh myvm1 "docker swarm leave -f" # Make master leave, kill swarm
docker-machine ls # list VMs, asterisk shows which VM this shell is talking to
docker-machine start myvm1            # Start a VM that is currently not running
docker-machine env myvm1      # show environment variables and command for myvm1
eval $(docker-machine env myvm1)         # Mac command to connect shell to myvm1
& "C:\Program Files\Docker\Docker\Resources\bin\docker-machine.exe" env myvm1 | Invoke-Expression   # Windows command to connect shell to myvm1
docker stack deploy -c <file> <app>  # Deploy an app; command shell must be set to talk to manager (myvm1), uses local Compose file
docker-machine scp docker-compose.yml myvm1:~ # Copy file to node's home dir (only required if you use ssh to connect to manager and deploy the app)
docker-machine ssh myvm1 "docker stack deploy -c <file> <app>"   # Deploy an app using ssh (you must have first copied the Compose file to myvm1)
eval $(docker-machine env -u)     # Disconnect shell from VMs, use native docker
docker-machine stop $(docker-machine ls -q)               # Stop all running VMs
docker-machine rm $(docker-machine ls -q) # Delete all VMs and their disk images
```