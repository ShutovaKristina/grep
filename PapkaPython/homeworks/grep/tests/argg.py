import argparse,sys


parser = argparse.ArgumentParser()

parser.add_argument('-1', '--one', action='store_true', help='This will be option One')
parser.add_argument(
        '-v', action="store_true", dest="invert", default=False, help='Selected lines are those not matching pattern.')
print(parser.parse_args(sys.argv[1:]))
res = parser.parse_args(sys.argv[1:])

if res.invert:
        print('First is True!')
else:
        print('First is nothing :-(')

