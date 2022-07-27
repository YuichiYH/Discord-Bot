from src.setup import client

with open("token.txt", "r") as token:
    client.run(token.read())