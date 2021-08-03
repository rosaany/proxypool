from processor import Processor
import argparse

parser = argparse.ArgumentParser(description="Proxypool")
parser.add_argument('--processor', type=str, help='run a processor')
args = parser.parse_args()

if __name__ == '__main__':
    process = Processor()
    if args.processor:
        getattr(process, f'run_{args.processor}')()
    else:
        process.run
