# Containers

## Virtual machine vs. containers

Virtual machine is like a complete another computer on the same HW with different Operating system. It has lot of overhead. Performance is bad, since the same HW is used. The virtual machine needs to be setup, which is high effort.

Containers run on Docker engine and is much smaller than the whole opersting system. The container has only what is really necessary SW packages. It still uses the host Os ressources. The container can be built into an image and shered with others.

## Docker setup

Linux doesn't need those tools and you can directly install the Docker-Engine and then you can directly run the `docker` command. 

Install Docker-Desktop - is recommended. If you can't use Docker-Desktop install Docker-Toolbox on Windows. Docker-Desktop is a GUI, which starts the Docker engine. On Windows Contanirization needs to be activated. At the end you setup a Linux system on Windows. Best to setup Linux for Contanirization.

Check out [Docker Playground](https://labs.play-with-docker.com/)

## Docker 

To build a container you need a set of instructions in your project. Those instructions you store in a _Dockerfile_. 
With `docker build .` the container will be built according to the instructions. The container will have an id and it can be used to run the image like this `docker run -p3000:3000 123456789`. `-p 3000` is the port number.

> To stop a running container you need to start another comand line promt an check the running containers and the execute a command to stop it.

**Images** are templates/blue prints to build containers. We run concrete containers, which share the same image. Images contain tools and code. 

To start with building a container we need an image. We can use one existing e.g. [python image](https://hub.docker.com/_/python/)
You can checkout the docker-hub for existing images. You can use an existing image and build up an own image. 

Instruction in the _Dockerfile_ to create an **image**:

```docker
# FROM - allows you to build an image, based on another image. Use the name of the image, which exists locally or on Docker-hub
FROM python

# WORKDIR - to setup the working directory, where the commands will be executed
WORKDIR /app

# COPY - says which files shall be put into the container. /app is the target folder in the container. . is the same location where the Dockerfile is
COPY . /app

# RUN - to run a command
RUN uv sync

# EXPOSE what to be exposed from the Container to the local system
EXPOSE 80

# CMD registers commands, which can run in a container - is the last command
CMD ["python", "main.py"]
```
Image isn't started - it is not a container.

`docker build .` to build a container with the instruction from the _Dockerfile_. 
`docker build -t name:tag .` will build the image with the name=name and the tag=tag.

The container is executing the commandaccording to the instruction, when it is started:

`docker run -p 3000:80 123456789`, where `-p` is a flag for publishing the port: 3000 is the local host port, under which we want to reach the container and 80 ist the exposed port of the container.
> `docker run` always create a new container. With `docker start 12345566889` can restart the existing container.
## Container Layers

Every instruction is cached and is a layer. If one layer needs to be executed, other layers will be reexecuted. Possible optimization:

```docker
FROM python

WORKDIR /app

# if this file doesn't change - no need to run uv sync -> will take form cache
COPY project.toml /app

RUN uv sync

COPY . /app

# EXPOSE what to be exposed from the Container to the local system
EXPOSE 80

# CMD registers commands, which can run in a container - is the last command
CMD ["python", "main.py"]
``` 

## mscelaneous

You need to clea your containers from time to time: `docker rm name1 name2`
If you want to remove an image, you must remove first the containrs, which were built from this image.
To removed the stopped container automatically use `--rm` tag: `docker run -p 3000:80 --rm 123456789` 