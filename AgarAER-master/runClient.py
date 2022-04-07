from network.client import NetworkClient
from network.messaging import AuthenticationRequest
import dill as pickle
import logging

def run():
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(filename)s:%(funcName)s - %(message)s')
    client = NetworkClient()
    client.initConnectionToServer('omaior',lambda c : print(c['player']))
   #client.listenToGameChannel(6000,lambda c : print(c))


if __name__ == '__main__':
    run()