class Shelve:
    """
        Esta classe tem como função ser uma cache indivual para um determinado grupo multicast em uma determinada porta
        esta guarda o payload do pacote ,num dicionario em que o hash vai ser o message digest do payload
        De x em x tempo limpa a cache
    """
    def __init__(self,group_addr,port):
        pass