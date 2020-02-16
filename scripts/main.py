import argparse
import itertools
import os
import sys
from typing import Dict

from sqlalchemy import create_engine, MetaData, Table


def _batch_iter(n, iterable):
    it = iter(iterable)
    while True:
        batch = list(itertools.islice(it, n))
        if not batch:
            return
        yield batch


def _generate_fake(key, value, mapping):
    return mapping[key](value)


def run(source_engine_url, target_engine_url, batch_size, mapping_py):
    mapping_py_file = import_mapping_py(mapping_py)
    mapping = mapping_py_file.mapping
    source_engine = create_engine(source_engine_url)
    target_engine = create_engine(target_engine_url)
    source_metadata = MetaData()
    source_metadata.reflect(bind=source_engine)
    source_tables: Dict[str, Table] = source_metadata.tables

    # First copy all tables
    for table_name, table in source_tables.items():
        table.create(bind=target_engine, checkfirst=True)

    # Copy data
    target_metadata = MetaData()
    target_metadata.reflect(bind=target_engine)
    target_tables: Dict[str, Table] = target_metadata.tables
    for table_name, target_table in target_tables.items():
        source_table: Table = source_tables[table_name]
        query = source_table.select().execution_options(stream_results=True)
        for batch_id, batch in enumerate(_batch_iter(batch_size, source_engine.execute(query))):
            rows = [{key: mapping[key.lower()](value) for (key, value) in row.items()} for row in batch]
            print(f"Fetched batch_id: {batch_id} with size {len(rows)}")
            target_engine.execute(target_table.insert(values=rows))
            print(f"Inserted batch_id: {batch_id} with size {len(rows)}")


def import_mapping_py(mapping_py):
    directory, module_name = os.path.split(mapping_py)
    module_name = os.path.splitext(module_name)[0]
    path = list(sys.path)
    sys.path.insert(0, directory)
    module = __import__(module_name)
    return module


if __name__ == "__main__":
    desc = "A simple python tool to generate fake data from production data," \
           " while copying it to local database."
    epilog = "Fibber uses sqlalchemy, refer https://docs.sqlalchemy.org/en/13/core/engines.html"
    parser = argparse.ArgumentParser(description=desc, epilog=epilog)
    parser.add_argument("--source_engine_url", required=True, help="sqlalchemy create_engine() connection string")
    parser.add_argument("--target_engine_url", required=True, help="sqlalchemy create_engine() connection string")
    parser.add_argument("--batch_size",
                        required=False,
                        help="Batch size for copying to target engine",
                        default=1000
                        )
    parser.add_argument("--mapping_py", required=True, help="Python file with column to fake generator mapping")
    args = parser.parse_args()

    run(
        args.source_engine_url,
        args.target_engine_url,
        args.batch_size,
        args.mapping_py
    )
