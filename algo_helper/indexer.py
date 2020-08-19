# -*- coding: utf-8 -*-
# =================================== Meta ================================== #
'''
Author: Ankit Murdia
Contributors:
Version: 0.0.1
Created: 2020-08-15 12:30:56
Updated: 2020-08-19 23:46:53
Description:
Notes:
To do:
'''
# =========================================================================== #


# =============================== Dependencies ============================== #
import os
import os.path
import pkgutil
import importlib
import re
import string
import hashlib
import asyncio
import aiosqlite
import uuid
import argparse
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

import config
import problems
from helpers.log_helper import log as logging
# =========================================================================== #


# ================================ Constants ================================ #
logger = logging.getLogger(__name__)
problem_pattern = "problem:(.*)"
tag_pattern = "tags:(.*)"
time_pattern = "time:(.*)"
space_pattern = "space:(.*)"
# =========================================================================== #


# ================================ Code Logic =============================== #
#  Callable methods
async def get_sources(package):
    try:
        for importer, modname, ispkg in pkgutil.iter_modules(package.__path__):
            if ispkg:
                importlib.import_module(".".join([package.__name__, modname]))
                yield getattr(package, modname)

    except Exception as e:
        raise e


async def get_problems(package):
    try:
        async for source in get_sources(package):
            for importer, modname, ispkg in pkgutil.iter_modules(source.__path__):
                if ispkg:
                    logger.error("module expected, package found ({})".format(modname))
                    raise Exception("module expected, package found ({})".format(modname))

                importlib.import_module(".".join([package.__name__, source.__name__, modname]))
                yield source, getattr(source, modname)

    except Exception as e:
        raise e


async def extract_tags(problem):
    try:
        tokens = [word.lower() for word in word_tokenize(problem)]
        table = str.maketrans('', '', string.punctuation)
        stop_words = set(stopwords.words('english'))
        words = []

        for t in tokens:
            stripped = t.translate(table)

            if stripped.isalpha() and stripped not in stop_words:
                words.append(stripped)

        return words

    except Exception as e:
        raise e


async def get_data(package):
    try:
        async for source, problem_module in get_problems(package):
            problem_statement = "Unknown"
            tags = [source.__name__, problem_module.__name__]
            time = "Unknown"
            space = "Unknown"
            func = getattr(problem_module, "main")

            result1 = re.findall(problem_pattern, func.__doc__)
            result2 = re.findall(tag_pattern, func.__doc__)
            result3 = re.findall(time_pattern, func.__doc__)
            result4 = re.findall(space_pattern, func.__doc__)

            if result1:
                problem_statement = result1[0].strip()
                tags += await extract_tags(problem_statement)

            if result2:
                tags += [t.strip() for t in result2[0].split(',')]

            if result3:
                time = result3[0].strip()

            if result4:
                space = result4[0].strip()

            yield source.__name__, problem_module.__name__, tags, problem_statement, time, space

    except Exception as e:
        raise e


async def update_index():
    try:
        async for source, problem, tags, problem_statement, time, space in get_data(problems):
            path = os.path.join(config.problem_dir, source, problem+".py")
            key = "{}::{}::{}::{}::{}".format(source, ",".join(tags), problem_statement, time, space)
            md5sum = hashlib.md5(key.encode()).hexdigest()

            async with aiosqlite.connect(config.db) as db:
                cursor = await db.execute("select id, hash from search_index where source='?' and file='?'", [source, path])
                row = await cursor.fetchone()
                await cursor.close()

                if row and row[1] != md5sum:
                    rowid = row[0]
                    await db.execute("update data_map set problem='?', space='?', time='?', hash='?' where source='?' and file='?'", [problem_statement, space, time, md5sum, source, path])

                elif not row:
                    rowid = str(uuid.uuid4())
                    await db.execute("insert into data_map(id, source, file, space, time, problem, hash) values('?', '?', '?', '?', '?', '?', '?')", [rowid, source, path, space, time, problem_statement, md5sum])

                else:
                    continue

                tag_len = len(tags)
                await db.execute("insert into tag_map(tag, data_id) values " + ",".join(["('?', '?')" for i in tag_len]) + " on conflict ignore", list(zip(tags, [rowid]*tag_len)))
                await db.execute("delete from tag_map where tag not in ('')".format("','".join(tags)))
                await db.commit()

    except Exception as e:
        raise e


async def rebuild_index():
    try:
        async with aiosqlite.connect(config.db) as db:
            await db.execute("delete from tag_map")
            await db.execute("delete from data_map")
            await db.commit()

        await update_index()

    except Exception as e:
        raise e


#  Abstracted classes

# =========================================================================== #


# =============================== CLI Handler =============================== #
if __name__ == "__main__":
    dispatcher = {
        'update_index': update_index,
        'rebuild_index': rebuild_index
    }

    parser = argparse.ArgumentParser()
    parser.add_argument("func", type=str, choices=dispatcher.keys(), help="Method to use - {}".format(", ".join(dispatcher.keys())))
    args = parser.parse_args()

    asyncio.run(dispatcher[args.func]())
# =========================================================================== #