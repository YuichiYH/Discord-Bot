from src.setup import client

token = open("token.txt", "r")

client.run(token.read())