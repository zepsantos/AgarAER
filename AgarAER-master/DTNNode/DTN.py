from dtnnode import DTNNode
import argparse
import logging
def run():
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s - %(levelname)s - %(filename)s:%(funcName)s - %(message)s')
    parser = argparse.ArgumentParser()
    parser.add_argument('--i', type=str, required=True)
    parser.add_argument('--o', type=str)
    args = parser.parse_args()
    print(args)
    if args.o is None:
        dtnnode = DTNNode(False,args.i)
    else:
        dtnnode = DTNNode(True,args.i)    
    
    dtnnode.start()


run()