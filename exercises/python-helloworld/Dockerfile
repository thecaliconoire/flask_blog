# use the golang:alpine base image
FROM python:3.8


# copy all the files from the current directory to the container working directory (e.g. `/go/src/app`)
COPY . /app

# set the working directory to /go/src/app
WORKDIR /app

# import dependencies using `go mod init` and build the application using `go build -o helloworld` command, where `-o helloworld` will create the binary of the application with the name `helloworld`
RUN pip install -r requirements.txt


# start the container by invoking the binary created earlier, which is  `./helloworld`
CMD ["python", "app.py"]