"""Script to test some snippets"""

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("square", type=int,
                    help="display a square of a given number")
parser.add_argument("-v", "--verbosity", type=int,
                    help="increase output verbosity")
args = parser.parse_args()
answer = args.square**2
if args.verbosity == 2:
    print(f"the square of {args.square} equals {answer}")
elif args.verbosity == 1:
    print(f"{args.square}^2 == {answer}")
else:
    print(answer)
# parser = argparse.ArgumentParser(prog='zabbix_iber.py')
# parser.add_argument('credentials', type=str,
#                     help='file containing the i-DE credentials')
# parser.add_argument('-d', '--day',
#                     help='day you want to ask (format: %d-%m-%Y)')
# args = parser.parse_args()
