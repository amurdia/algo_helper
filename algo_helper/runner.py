# -*- coding: utf-8 -*-
# =================================== Meta ================================== #
'''
Author: Ankit Murdia
Contributors:
Version: 0.0.1
Created: 2020-08-15 12:30:51
Updated: 2020-08-19 23:25:59
Description:
Notes:
To do:
'''
# =========================================================================== #


# =============================== Dependencies ============================== #
import argparse
import cProfile, pstats, io
import problems
import importlib

from helpers.log_helper import log as logging
# =========================================================================== #


# ================================ Constants ================================ #
logger = logging.getLogger(__name__)
# =========================================================================== #


# ================================ Code Logic =============================== #
#  Callable methods
def parse_val(arg, splitter):
    try:
        list_val = [v.strip() for v in arg.split(splitter)]
        sv = len(list_val)

        if all(map(lambda x: x.isdigit() or (len(x) >= 1 and x[0]=='-' and x[1:].isdigit()), list_val)):
            val_type = 'int'

        elif all(map(lambda x: x.isdigit() or (len(x) >= 1 and x.split('.')[0].isdigit() and x.split('.')[1].isdigit()), list_val)):
            val_type = 'float'

        else:
            val_type = 'str'

        list_val_new = list(map(eval(val_type), list_val))
        return list_val_new if len(list_val_new) > 1 else list_val_new[0]

    except Exception as e:
        raise e


def parse_file(file):
    try:
        func_args = []

        with open(file) as fh:
            for line in fh:
                if line.strip() == "":
                    yield func_args

                    func_args = []
                    continue

                func_args.append(parse_val(line.strip(), ' '))

    except Exception as e:
        raise e


def main(source, problem, args, output=None):
    try:
        module = importlib.import_module("problems.{}.{}".format(source, problem))

        pr = cProfile.Profile()
        pr.enable()
        result = getattr(module, 'main')(*args)
        pr.disable()

        s = io.StringIO()
        ps = pstats.Stats(pr, stream=s)
        ps.print_stats()

        if output:
            with open(output, "a") as fh:
                fh.write("Result: {}\n\n".format(result))
                fh.write(s.getvalue())
                fh.write("\n===================================================\n\n")

        else:
            print("Result: {}\n\n".format(result))
            print(s.getvalue())
            print("\n===================================================\n\n")

    except Exception as e:
        raise e


#  Abstracted classes

# =========================================================================== #


# =============================== CLI Handler =============================== #
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=str, help="Source platform for the problem. Eg. leetcode, hackerrank, etc.")
    parser.add_argument('problem', metavar='p', type=str, help="problem program to run.")
    parser.add_argument('args', metavar='a', type=str, nargs="*", help="function arguments.")
    parser.add_argument('-f', "--file", type=str, help="Input file.")
    parser.add_argument('-o', "--output", type=str, help="Output file.")
    parser.add_argument('-v', "--verbose", action="store_true", help="Verbose output.")
    args = parser.parse_args()

    if getattr(args, 'file', None):
        for func_args in parse_file(args.file):
            main(args.source, args.problem, func_args, getattr(args, 'output', None), args.verbose)

    else:
        func_args = []
        kwargs = vars(args)

        for a in kwargs['args']:
            func_args.append(parse_val(a, ','))

        main(kwargs['source'], kwargs['problem'], func_args, getattr(args, 'output', None), kwargs['verbose'])
# =========================================================================== #