from logging import exception

from matplotlib.streamplot import InvalidIndexError
from src.setup import client
from os import listdir

try:
    token_path = "token/" + listdir("token")[0]

    with open(token_path, "r") as token:
        client.run(token.read())

except IndexError:
    print("Cound't log into bot, missing token")