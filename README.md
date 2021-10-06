# pictureinspector-bot

# Installation

## Python installation
To run this server you need to install [Python3+](https://realpython.com/installing-python/).
And [pip](https://pip.pypa.io/en/stable/installation/).

## Libraries installation
Install all needed libraries using this command:
```shell script
> pip3 install -r requirements.txt
```

## Setting up telegram bot token and server url
Create file named .env in project directory and write telegram bot token and server url. Your .env file should be the following:
```text
TG_TOKEN=Your telegram bot token
SERVER_ADDR=Url to server with neural network
```
Example of .env file:
```text
TG_TOKEN=0000000000:AAAaaaaaaaaaaa-AAAAAA-AAAaaaaaaaaa
SERVER_ADDR=https://127.0.0.1:5000/api/v1/pictures
```

# Running
Write following command
```shell script
> python3 main.py
```
