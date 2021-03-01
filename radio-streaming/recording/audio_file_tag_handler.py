from datetime import datetime
from typing import Dict


class AudioTagHandler(object):
    def __init__(self):
        pass

    def tag_file(self, file_path: str, start_time: datetime, end_time: datetime) -> bool:
        pass

    def get_file_information(self, file_path: str) -> Dict:
        pass
