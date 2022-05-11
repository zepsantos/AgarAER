from network.server import Server
import logging
def run():
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(filename)s:%(funcName)s - %(message)s')
    server = Server()
    server.start_listening()



if __name__ == '__main__':
    run()