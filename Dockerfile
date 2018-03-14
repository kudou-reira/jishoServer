FROM jfloff/alpine-python:latest

MAINTAINER kudou-reira

# Update
RUN apk add --update python3 py-pip 

# Install app dependencies
RUN pip3 install Flask

# Bundle app source
COPY . /src

WORKDIR /src

RUN pip3 install -r requirements.txt

EXPOSE  8080
ENTRYPOINT ["python3"]
CMD ["index.py"]