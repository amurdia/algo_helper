# -*- coding: utf-8 -*-
# =================================== Meta ================================== #
'''
Author: Ankit Murdia
Contributors:
Version: 0.0.1
Created: 2020-08-15 12:30:56
Updated: 2020-08-20 01:55:05
Description:
Notes:
To do:
'''
# =========================================================================== #


# =============================== Dependencies ============================== #
import asyncio
import aiosqlite
import argparse
import json
import os.path
from texttable import Texttable

import config
import problems
from helpers.log_helper import log as logging
# =========================================================================== #


# ================================ Constants ================================ #
logger = logging.getLogger(__name__)
SHOW_HEADERS = [
    'source',
    'tags',
    'name',
    'file',
    'problem',
    'time complexity',
    'space complexity',
    'match accuracy',
    'test file',
    'test case count'
]
MAX_ROW_WIDTH = 150
# =========================================================================== #


# ================================ Code Logic =============================== #
#  Callable methods

#  Abstracted classes
async def main(**kwargs):
    try:
        query = "select dm1.source, t.tags, dm1.file, dm1.problem, dm1.`time`, dm1.space, t.accuracy from (select dm.id, group_concat(tm.tag, ', ') tags, round(count(tm.tag)*100.0/{taglength}, 2) accuracy from data_map dm inner join tag_map tm on tm.data_id=dm.id where {condition} group by dm.id) t inner join data_map dm1 on t.id=dm1.id order by t.accuracy desc limit {limit};"
        condition = ""

        " dm.source='{}' or tm.tags in ('{}') dm.file='{}';"

        if kwargs.get('source'):
            condition = "dm.source='{}'".format(kwargs['source'])

        if kwargs.get('tags'):
            condition = (condition and (condition +" and ")) + "tm.tag in ('{}')".format(kwargs['tags'])

        if kwargs.get('file'):
            condition = (condition and (condition +" and ")) + "dm.file like '%{}%'".format(kwargs['file'])

        if kwargs.get('time'):
            condition = (condition and (condition +" and ")) + "dm.`time`='{}'".format(kwargs['time'])

        if kwargs.get('space'):
            condition = (condition and (condition +" and ")) + "dm.space='{}'".format(kwargs['space'])

        query = query.format(
                    condition=condition,
                    taglength=len([t.strip() for t in kwargs.get('tags', "").split(',')]) or "count(tm.tag)",
                    limit=(kwargs.get('n', 0) > 0 and kwargs['n']) or 50
                )

        final_result = []

        async with aiosqlite.connect(config.db) as db:
            async with db.execute(query) as cursor:
                async for row in cursor:
                    file_name = ".".join(os.path.basename(row[2]).split('.')[:-1])
                    test_file_name = file_name + ".tc"
                    test_file_path = os.path.join(os.path.dirname(row[2]), test_file_name)
                    test_case_count = 0

                    with open(test_file_path) as fh:
                        for line in fh:
                            if line.strip() == "":
                                test_case_count += 1

                    data_dict = {
                                    'source': row[0],
                                    'tags': row[1],
                                    'name': ".".join(os.path.basename(row[2]).split('.')[:-1]),
                                    'file': row[2],
                                    'problem': row[3],
                                    'time complexity': row[4],
                                    'space complexity': row[5],
                                    'match accuracy': str(row[6]) + "%",
                                    'test file': test_file_path,
                                    'test case count': test_case_count
                                }

                    if kwargs.get('args'):
                        formatted_data_dict = {k: data_dict.get(k, None) for k in kwargs['args']}
                        final_result.append(formatted_data_dict)

                    else:
                        final_result.append(data_dict)

        if kwargs.get('j'):
            print(json.dumps(final_result, indent=4))

        table = Texttable()
        texttable.set_max_width(MAX_ROW_WIDTH)
        headers = list(kwargs.get('args', SHOW_HEADERS))
        data = [[row[k] for k in headers] for row in final_result]
        table.add_rows([headers] + data)
        print(table.draw() + "\n")

        await cursor.close()
        await db.commit()

    except Exception as e:
        raise e
# =========================================================================== #


# =============================== CLI Handler =============================== #
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("func", type=str, help="Operation to perform.")
    parser.add_argument('-s', '--source', type=str, help="Source platform for the problem. Eg. leetcode, hackerrank, etc.")
    parser.add_argument('-t', '--tags', type=str, help=", separated list of tags to search.")
    parser.add_argument('-f', '--file', type=str, help="file path/name to search.")
    parser.add_argument('-i', '--time', type=str, help="Time complexity.")
    parser.add_argument('-p', '--space', type=str, help="Space complexity.")
    parser.add_argument('-a', "--args", type=str, help=", separated list of arguments to be displayed.")
    parser.add_argument('-j', action="store_true", help="Output as json. If not set, output will be a text table.")
    parser.add_argument('-n', type=int, help="Number of records to be displayed. Default: 50.")
    kwargs = vars(parser.parse_args())

    # if not (kwargs.get('args') or kwargs.get('source')):
    #     raise Exception("Need atleast a source or a tag to search.")

    asyncio.run(main(**kwargs))
# =========================================================================== #