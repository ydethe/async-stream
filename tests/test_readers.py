import os
from pathlib import Path
import sys
from tempfile import NamedTemporaryFile

import pytest

import asyncstream

sys.path.insert(0, str(Path(__file__).parent))

from test_utils import async_gen_to_list, get_raw_rows, compress


@pytest.mark.parametrize("compression", [None, "gzip", "bzip2", "zstd"])
@pytest.mark.asyncio
async def test_reader(compression: str):
    baby_name_filename = os.path.join(os.path.dirname(__file__), "data", "baby_names.csv")
    with NamedTemporaryFile() as tmpfd:
        tmpfd.write(compress(baby_name_filename, compression))
        tmpfd.flush()
        async with asyncstream.open(tmpfd.name, mode="rb", compression=compression) as fd:
            async with asyncstream.reader(fd) as reader:
                assert get_raw_rows(baby_name_filename) == await async_gen_to_list(reader)
