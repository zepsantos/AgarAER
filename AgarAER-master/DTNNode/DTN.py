from dtnnode import DTNNode
import argparse
import logging
import cProfile
def run():
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s - %(levelname)s - %(filename)s:%(funcName)s - %(message)s')
    parser = argparse.ArgumentParser()
    parser.add_argument('--i', type=str, required=True)
    parser.add_argument('--o', type=str)
    args = parser.parse_args()
    if args.o is None:
        dtnnode = DTNNode(False,args.i, None)
    else:
        tmplist = args.o.split(',')
        logging.debug(f'interfaces args {tmplist}')
        dtnnode = DTNNode(True,args.i,args.o)
    
    dtnnode.start()

run()
