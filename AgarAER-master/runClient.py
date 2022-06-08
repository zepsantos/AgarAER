import time

from network.client import NetworkClient
from network.messaging import AuthenticationRequest
import dill as pickle
import logging

def run():
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(filename)s:%(funcName)s - %(message)s')
    global client
    client = NetworkClient()
    client.initConnectionToServer('omaior',teste)
    client.listenToGameChannel(6000,lambda c : print(c))
def teste(c):
    while c == {}:
        print('vazio')
        time.sleep(1)
        client.initConnectionToServer('omaior',teste)
    print(c['player'])

if __name__ == '__main__':
    run()