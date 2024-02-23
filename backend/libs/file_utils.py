import json
import os

from pathlib import Path
from typing import Generator
from libs.time_utils import TimeUtils
from typing import Any
from pprint import pprint


class FileUtils:
    @classmethod
    def save_json(cls: 'FileUtils', data: any, prefix: str = '') -> str:
        local_filename = f'{prefix}{TimeUtils.get_now_datetime_str()}.json'
        with open(local_filename, 'w') as out_file:
            out_file.write(json.dumps(data, ensure_ascii=False))
        return local_filename

    @classmethod
    def clear_file(cls: 'FileUtils', filename: str) -> None:
        if os.path.exists(filename):
            os.remove(filename)
        else:
            pprint(f"Can not delete the file: {filename} as it doesn't exists")

    @classmethod
    def iter_dir(cls: 'FileUtils', path: str) -> Generator[Path, Any, None]:
        for child in Path(path).iterdir():
            if not child.is_dir():
                yield child
