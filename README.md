## Fibber

A simple python tool to generate fake data from production data, while copying it to local database.

## Usage

```shell script
usage: main.py [-h] --source_engine_url SOURCE_ENGINE_URL --target_engine_url TARGET_ENGINE_URL [--batch_size BATCH_SIZE] --mapping_py MAPPING_PY

A simple python tool to generate fake data from production data, while copying it to local database.

optional arguments:
  -h, --help            show this help message and exit
  --source_engine_url SOURCE_ENGINE_URL
                        sqlalchemy create_engine() connection string
  --target_engine_url TARGET_ENGINE_URL
                        sqlalchemy create_engine() connection string
  --batch_size BATCH_SIZE
                        Batch size for copying to target engine
  --mapping_py MAPPING_PY
                        Python file with column to fake generator mapping

Fibber uses sqlalchemy, refer https://docs.sqlalchemy.org/en/13/core/engines.html
```

### Setting up the demo
The demo contains a `customer` table in `fibber_demo_source` postgres db.

After running fibber you can find a similar `customer` table in `fibber_demo_target` postgres db

But, the data will be faked.

You should have postgres installed
```shell script
# Create conda environemnt
conda env create -f environment.yml
# Setup data
psql -f scripts/demo/run.psql
# Run fibber
python scripts/main.py --source_engine_url postgresql://localhost:5432/fibber_demo_source --target_engine_url postgresql://localhost:5432/fibber_demo_target --mapping_py scripts/mapping_py
```