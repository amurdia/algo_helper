# -*- coding: utf-8 -*-
# =================================== Meta ================================== #
'''
Author: Ankit Murdia
Contributors:
Version: 0.0.1
Created: 2020-08-15 12:30:51
Updated: 2020-08-20 02:39:22
Description:
Notes:
To do:
'''
# =========================================================================== #


# =============================== Dependencies ============================== #
import os
import argparse
import cProfile, pstats, io
import problems
import importlib
import hashlib
from contextlib import contextmanager

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


def update_test_case(tcfh, args):
    try:
        for a in args:
            if type(a) in (list, tuple):
                tcfh.write(" ".join(a))

            else:
                tcfh.write(a)

            tcfh.write("\n")

        tcfh.write("\n")

    except Exception as e:
        raise e

def clean_test_cases(path):
    try:
        bkp_path = path+".bkp"
        hash_map = {}
        group = ""

        print("Test Case cleaning in progress...", end="")

        with open(path) as rfh, open(bkp_path, 'w') as wfh:
            for line in rfh:
                if line.strip() == "":
                    md5sum = hashlib.md5(group.encode()).hexdigest()

                    if not hash_map.get(md5sum):
                        wfh.write(group + "\n")

                    hash_map.setdefault(md5sum, 0)
                    hash_map[md5sum] += 1
                    group = ""
                    continue

                group += line + "\n"

        os.remove(path)
        os.rename(bkp_pathm, path)
        print("\rCleanup completed with {} duplicate test cases.\n".format(sum(hash_map.values())-len(hash_map)))

    except Exception as e:
        raise e


def main(module, args, output=None):
    try:
        pr = cProfile.Profile()
        pr.enable()
        result = getattr(module, 'main')(*self.args)
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
    parser.add_argument('-c', "--cleanup", action="store_true", help="Cleanup test case file after execution is completed.")
    args = parser.parse_args()

    module = importlib.import_module("problems.{}.{}".format(source, problem))
    modpath = module.__path__
    test_file_name = problem + ".tc"
    test_file_path = os.path.join(os.path.dirname(modpath), test_file_name)

    with open(test_file_path, "a") as tcfh:
        if getattr(args, 'file', None):
            for func_args in parse_file(args.file):
                update_test_case(tcfh, func_args)
                main(module, func_args, getattr(args, 'output', None), args.verbose)

        else:
            func_args = []
            kwargs = vars(args)

            for a in kwargs['args']:
                func_args.append(parse_val(a, ','))

            update_test_case(tcfh, func_args)
            main(module, func_args getattr(args, 'output', None), kwargs['verbose'])

    if args.cleanup:
        clean_test_cases(test_file_path)
# =========================================================================== #